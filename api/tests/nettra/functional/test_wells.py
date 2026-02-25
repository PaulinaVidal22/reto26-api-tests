import pytest

from api.models.nettra.well_models import WellsListResponse
from api.models.nettra.error_models import ErrorResponse
from api.builders.nettra.wells_query_builder import WellsQueryBuilder


INVALID_WELL = "00000000-0000-0000-0000-000000000000"


# ==========================================================
# SUCCESS CASES
# ==========================================================

@pytest.mark.nettra
@pytest.mark.smoke
@pytest.mark.functional
def test_list_wells_success(nettra_client, nettra_token):
    response = nettra_client.get(
        "/wells/",
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 200

    parsed = WellsListResponse.model_validate(response.json())

    assert parsed.total >= len(parsed.items)

    for well in parsed.items:
        assert well.name
        assert well.device_id

@pytest.mark.nettra
@pytest.mark.functional
def test_list_wells_custom_pagination(nettra_client, nettra_token):
    query = (
        WellsQueryBuilder()
        .with_pagination(page=1, page_size=2)
        .build()
    )

    response = nettra_client.get(
        "/wells/",
        params=query,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 200

    parsed = WellsListResponse.model_validate(response.json())

    assert parsed.page == 1
    assert parsed.page_size == 2
    assert len(parsed.items) <= 2

@pytest.mark.nettra
@pytest.mark.functional
def test_list_wells_search_by_name(nettra_client, nettra_token):
    query = (
        WellsQueryBuilder()
        .with_search("Well A")
        .build()
    )

    response = nettra_client.get(
        "/wells/",
        params=query,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 200

    parsed = WellsListResponse.model_validate(response.json())

    assert parsed.total >= 1
    assert any("Well A" in well.name for well in parsed.items)

# ==========================================================
# NEGATIVE  CASES
# ==========================================================

@pytest.mark.nettra
@pytest.mark.functional
def test_list_wells_invalid_pagination(nettra_client, nettra_token):
    query = (
        WellsQueryBuilder()
        .with_pagination(page=0, page_size=200)
        .build()
    )

    response = nettra_client.get(
        "/wells/",
        params=query,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 400

    error = ErrorResponse.model_validate(response.json())

    assert error.error.code == "INVALID_PAGINATION"

@pytest.mark.nettra
@pytest.mark.security
@pytest.mark.functional
@pytest.mark.parametrize(
    "headers_override",
    [
        {"Authorization": "Bearer invalid.token.value"},
        {"Authorization": None},
    ],
)
def test_list_wells_auth_errors(nettra_client, headers_override):
    response = nettra_client.get(
        "/wells/",
        headers_override=headers_override
    )

    assert response.status_code == 401