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
        path="/wells/{well_id}",
        method="GET",
    )
)


@pytest.mark.nettra
@pytest.mark.contract
@pytest.mark.slow
@pytest.mark.flaky(reruns=2)
@schema.parametrize()
def test_well_detail_contract(
    case,
    nettra_token,
    existing_well_id,
):
    """
    Valida que GET /wells/{well_id}
    cumple con el contrato OpenAPI.
    """

    case.path_parameters["well_id"] = existing_well_id

    execute_contract_case(case, nettra_token)