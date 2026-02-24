import httpx
import pytest


NON_EXISTENT_WELL_ID = "00000000-0000-0000-0000-000000000000"


def _extract_first_well_id(payload):
    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                for key in ("id", "well_id", "uuid"):
                    value = item.get(key)
                    if isinstance(value, str) and value:
                        return value
        return None

    if isinstance(payload, dict):
        for key in ("id", "well_id", "uuid"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value

        for key in ("items", "results", "data", "wells"):
            nested = payload.get(key)
            well_id = _extract_first_well_id(nested)
            if well_id:
                return well_id

    return None


def _assert_error_payload_not_html(response):
    content_type = response.headers.get("content-type", "").lower()
    if "application/json" in content_type:
        payload = response.json()
        if isinstance(payload, dict):
            assert any(key in payload for key in ("detail", "message", "error"))
        else:
            assert payload is not None
        return

    body = response.text.strip().lower()
    assert "<html" not in body


def _safe_get(client, url, params=None):
    try:
        return client.get(url, params=params)
    except httpx.HTTPError as exc:
        pytest.skip(f"No se pudo conectar a Nettra API: {exc}")


@pytest.fixture
def auth_headers(nettra_token):
    if not nettra_token:
        pytest.skip("NETTRA_TOKEN no definido; se omiten tests que requieren autenticación")
    return {"Authorization": f"Bearer {nettra_token}"}


@pytest.fixture
def valid_well_id(nettra_base_url, auth_headers):
    with httpx.Client(base_url=nettra_base_url, headers=auth_headers, timeout=10.0) as client:
        response = _safe_get(client, "/wells/", params={"page": 1, "page_size": 50})

    if response.status_code != 200:
        pytest.skip(f"No se pudo obtener un well_id válido desde /wells (status={response.status_code})")

    content_type = response.headers.get("content-type", "").lower()
    if "application/json" not in content_type:
        pytest.skip("El endpoint /wells no devolvió JSON")

    well_id = _extract_first_well_id(response.json())
    if not well_id:
        pytest.skip("No hay wells disponibles para ejecutar el test 200")

    return well_id


@pytest.fixture
def well_id_for_400(nettra_base_url, auth_headers):
    with httpx.Client(base_url=nettra_base_url, headers=auth_headers, timeout=10.0) as client:
        response = _safe_get(client, "/wells/", params={"page": 1, "page_size": 50})

    if response.status_code == 200:
        content_type = response.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            well_id = _extract_first_well_id(response.json())
            if well_id:
                return well_id

    return NON_EXISTENT_WELL_ID


@pytest.mark.nettra
def test_wells_measurements_200(nettra_base_url, auth_headers, valid_well_id):
    params = {
        "from": "2024-01-01T00:00:00",
        "to": "2024-12-31T23:59:59",
        "page": 1,
        "page_size": 200,
    }

    with httpx.Client(base_url=nettra_base_url, headers=auth_headers, timeout=10.0) as client:
        response = _safe_get(client, f"/wells/{valid_well_id}/parameter-measurements", params=params)

    assert response.status_code == 200
    assert "application/json" in response.headers.get("content-type", "").lower()

    payload = response.json()
    is_valid_shape = isinstance(payload, list) or (
        isinstance(payload, dict)
        and any(isinstance(payload.get(key), list) for key in ("items", "results", "data"))
    )
    assert is_valid_shape


@pytest.mark.nettra
def test_wells_measurements_401_without_auth(nettra_base_url):
    params = {
        "from": "2024-01-01T00:00:00",
        "to": "2024-12-31T23:59:59",
        "page": 1,
        "page_size": 200,
    }

    with httpx.Client(base_url=nettra_base_url, timeout=10.0) as client:
        response = _safe_get(client, f"/wells/{NON_EXISTENT_WELL_ID}/parameter-measurements", params=params)

    assert response.status_code == 401
    _assert_error_payload_not_html(response)


@pytest.mark.nettra
def test_wells_measurements_404_non_existent_well(nettra_base_url, auth_headers):
    params = {
        "from": "2024-01-01T00:00:00",
        "to": "2024-12-31T23:59:59",
        "page": 1,
        "page_size": 200,
    }

    with httpx.Client(base_url=nettra_base_url, headers=auth_headers, timeout=10.0) as client:
        response = _safe_get(client, f"/wells/{NON_EXISTENT_WELL_ID}/parameter-measurements", params=params)

    assert response.status_code == 404
    _assert_error_payload_not_html(response)


@pytest.mark.nettra
def test_wells_measurements_400_invalid_date_range(nettra_base_url, auth_headers, well_id_for_400):
    params = {
        "from": "2024-12-31T00:00:00",
        "to": "2024-01-01T00:00:00",
        "page": 1,
        "page_size": 200,
    }

    with httpx.Client(base_url=nettra_base_url, headers=auth_headers, timeout=10.0) as client:
        response = _safe_get(client, f"/wells/{well_id_for_400}/parameter-measurements", params=params)

    assert response.status_code == 400
    _assert_error_payload_not_html(response)
