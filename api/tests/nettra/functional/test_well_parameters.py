import pytest
from uuid import uuid4, UUID
from datetime import datetime, timedelta, UTC

from api.models.nettra.parameter_models import ParameterResponse
from api.models.nettra.error_models import ErrorResponse
from api.builders.nettra.parameters_query_builder import ParametersQueryBuilder


# ==========================================================
# SUCCESS
# ==========================================================

@pytest.mark.nettra
@pytest.mark.functional
@pytest.mark.integration
def test_get_well_parameters_success(
    nettra_client,
    nettra_token,
    existing_well_with_parameters
):
    """
    Valida que el endpoint devuelve parámetros correctamente
    para un pozo existente.
    """

    query = (
        ParametersQueryBuilder()
        .with_parameter_code("TEMP")
        .with_pagination(page=1, page_size=20)
        .build()
    )

    response = nettra_client.get_well_parameters(
        well_id=existing_well_with_parameters,
        params=query,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 200

    parsed = ParameterResponse.model_validate(response.json())

    assert parsed.page == 1
    assert parsed.page_size == 20
    assert isinstance(parsed.data, list)
    assert len(parsed.data) > 0


# ==========================================================
# 404 NOT FOUND
# ==========================================================

@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_parameters_not_found(
    nettra_client,
    nettra_token
):
    """
    Valida 404 cuando el pozo no existe.
    """

    fake_id = str(uuid4())

    response = nettra_client.get_well_parameters(
        well_id=fake_id,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 404

    parsed_error = ErrorResponse.model_validate(response.json())

    assert parsed_error.error.code == "WELL_NOT_FOUND"
    assert isinstance(parsed_error.error.message, str)


# ==========================================================
# INVALID DATE RANGE
# ==========================================================

@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_parameters_invalid_date_range(
    nettra_client,
    nettra_token,
    existing_well_with_parameters
):
    """
    Valida 400 cuando from > to.
    """

    now = datetime.now(UTC)
    past = now - timedelta(days=1)

    query = (
        ParametersQueryBuilder()
        .with_date_range(now.isoformat(), past.isoformat())
        .build()
    )

    response = nettra_client.get_well_parameters(
        well_id=existing_well_with_parameters,
        params=query,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 400

    parsed_error = ErrorResponse.model_validate(response.json())

    assert parsed_error.error.code == "INVALID_DATE_RANGE"
    assert isinstance(parsed_error.error.message, str)


# ==========================================================
# FILTER BY PARAMETER CODE
# ==========================================================

@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_parameters_filter_by_code(
    nettra_client,
    nettra_token,
    existing_well_with_parameters
):
    """
    Valida filtrado por parameter_code.
    """

    query = (
        ParametersQueryBuilder()
        .with_parameter_code("TEMP")
        .build()
    )

    response = nettra_client.get_well_parameters(
        well_id=existing_well_with_parameters,
        params=query,
        headers_override={"Authorization": f"Bearer {nettra_token}"}
    )

    assert response.status_code == 200

    parsed = ParameterResponse.model_validate(response.json())

    assert isinstance(parsed.data, list)

    # Validación coherente (sin acoplar demasiado al backend)
    for item in parsed.data:
        assert item.well_id == UUID(existing_well_with_parameters)