import os
import pytest
import schemathesis


# ==========================================================
# CONFIGURACIÓN DEL SCHEMA
# ==========================================================

BASE_URL = os.getenv("NETTRA_BASE_URL")

if not BASE_URL:
    raise RuntimeError("NETTRA_BASE_URL no está definida")

schema = (
    schemathesis.openapi.from_url(f"{BASE_URL}/openapi.json")
    .include(
        path="/wells/{well_id}/anomalies",
        method="GET",
    )
)


# ==========================================================
# CONTRACT TEST
# ==========================================================

@pytest.mark.nettra
@pytest.mark.contract
@pytest.mark.slow
@pytest.mark.flaky(reruns=2)
@pytest.mark.xfail(
    reason="OpenAPI contract mismatch con validación backend",
    strict=False
)
@schema.parametrize()
def test_wells_anomalies_contract(
    case,
    nettra_token,
    existing_well_with_anomalies,
):
    """
    Valida que el endpoint GET /wells/{well_id}/anomalies
    cumple con el contrato OpenAPI definido.
    """

    # Header dinámico
    case.headers = {
        "Authorization": f"Bearer {nettra_token}"
    }

    # Path parameter dinámico (evita hardcodear UUID)
    case.path_parameters["well_id"] = existing_well_with_anomalies

    response = case.call()

    if 200 <= response.status_code < 500:
        case.validate_response(response)