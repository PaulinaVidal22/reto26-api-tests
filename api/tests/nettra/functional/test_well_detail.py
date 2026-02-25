import pytest
from uuid import uuid4

from api.models.nettra.well_models import WellDetail
from api.models.nettra.error_models import ErrorResponse

# ==========================================================
# SUCCESS CASE
# ==========================================================
@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_detail_success(
    nettra_client,
    nettra_token,
    existing_well_id
):
    response = nettra_client.get(
        f"/wells/{existing_well_id}",
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 200

    parsed = WellDetail.model_validate(response.json())

    assert str(parsed.id) == existing_well_id
    assert parsed.name
    assert parsed.device_id

# ==========================================================
# 404 NOT FOUND CASE
# ==========================================================
@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_detail_not_found(nettra_client, nettra_token):
    fake_id = str(uuid4())

    response = nettra_client.get(
        f"/wells/{fake_id}",
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 404

    parsed = ErrorResponse.model_validate(response.json())

    assert parsed.error.code == "WELL_NOT_FOUND"

# ==========================================================
# AUTH ERRORS
# ==========================================================
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
def test_get_well_detail_auth_errors(
    nettra_client,
    existing_well_id,
    headers_override
):
    response = nettra_client.get(
        f"/wells/{existing_well_id}",
        headers_override=headers_override
    )

    assert response.status_code == 401
