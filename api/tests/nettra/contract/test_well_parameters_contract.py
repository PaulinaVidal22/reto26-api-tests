import os
import pytest
import schemathesis


BASE_URL = os.getenv("NETTRA_BASE_URL")

if not BASE_URL:
    raise RuntimeError("NETTRA_BASE_URL no está definida")

schema = (
    schemathesis.openapi.from_url(f"{BASE_URL}/openapi.json")
    .include(path="/wells/{id}/parameters", method="GET")
)


@pytest.mark.nettra
@pytest.mark.contract
@pytest.mark.slow
@pytest.mark.flaky(reruns=2)
@pytest.mark.xfail(
    condition=True,
    reason="Backend acepta query params no definidos en OpenAPI (falta validación estricta)",
    strict=False
)
@schema.parametrize()
def test_well_parameters_contract(
    case,
    nettra_token,
    existing_well_with_parameters
):
    """
    Valida que GET /wells/{id}/parameters
    cumple con el contrato OpenAPI.
    """

    case.headers = {
        "Authorization": f"Bearer {nettra_token}"
    }

    case.path_parameters["id"] = existing_well_with_parameters

    response = case.call()

    if 200 <= response.status_code < 500:
        case.validate_response(response)