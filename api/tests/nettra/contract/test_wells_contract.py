import os
import pytest
import schemathesis
from api.tests.nettra.contract._base_contract import execute_contract_case


BASE_URL = os.getenv("NETTRA_BASE_URL")

if not BASE_URL:
    raise RuntimeError("NETTRA_BASE_URL no está definida")


schema = (
    schemathesis.openapi.from_url(f"{BASE_URL}/openapi.json")
    .include(
        path="/wells/",
        method="GET",
    )
)


@pytest.mark.nettra
@pytest.mark.contract
@pytest.mark.slow
@pytest.mark.flaky(reruns=2)
@pytest.mark.xfail(
    condition=True,
    reason="Backend acepta query params no definidos en OpenAPI",
    strict=False
)
@schema.parametrize()
def test_wells_contract(
    case,
    nettra_token,
):
    """
    Valida que GET /wells
    cumple con el contrato OpenAPI.
    """

    execute_contract_case(case, nettra_token)