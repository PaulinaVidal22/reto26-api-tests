import pytest

from api.models.nettra.anomaly_models import AnomaliesResponse
from api.models.nettra.error_models import ErrorResponse
from api.builders.anomalies_builder import AnomaliesQueryBuilder


INVALID_WELL = "00000000-0000-0000-0000-000000000000"


# ==========================================================
# SUCCESS CASES
# ==========================================================

@pytest.mark.nettra
@pytest.mark.smoke
@pytest.mark.functional
def test_get_well_anomalies_success(
    nettra_client,
    existing_well_with_anomalies,
):
    response = nettra_client.get_well_anomalies(
        existing_well_with_anomalies
    )

    assert response.status_code == 200

    validated = AnomaliesResponse(**response.json())

    # Validaciones estructurales
    assert validated.pagination.total >= len(validated.data)

    # Validaciones de negocio básicas
    for anomaly in validated.data:
        assert anomaly.t_from <= anomaly.t_to
        assert anomaly.anomaly_code
        assert anomaly.anomaly_name


@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_anomalies_custom_pagination(
    nettra_client,
    existing_well_with_anomalies,
):
    builder = (
        AnomaliesQueryBuilder()
        .with_pagination(page=1, page_size=5)
    )

    response = nettra_client.get_well_anomalies(
        existing_well_with_anomalies,
        params=builder.build()
    )

    assert response.status_code == 200

    validated = AnomaliesResponse(**response.json())

    assert validated.pagination.page == 1
    assert validated.pagination.page_size == 5
    assert len(validated.data) <= 5


# ==========================================================
# NEGATIVE CASES
# ==========================================================

@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_anomalies_well_not_found(nettra_client):
    response = nettra_client.get_well_anomalies(INVALID_WELL)

    assert response.status_code == 404

    error = ErrorResponse(**response.json())
    assert error.error.code == "WELL_NOT_FOUND"


@pytest.mark.nettra
@pytest.mark.functional
def test_get_well_anomalies_invalid_date_range(
    nettra_client,
    existing_well_with_anomalies,
):
    builder = (
        AnomaliesQueryBuilder()
        .with_date_range(
            from_date="2026-02-16T10:00:00",
            to_date="2026-02-15T10:00:00",
        )
    )

    response = nettra_client.get_well_anomalies(
        existing_well_with_anomalies,
        params=builder.build()
    )

    assert response.status_code == 400

    error = ErrorResponse(**response.json())
    assert error.error.code == "INVALID_FILTERS"


@pytest.mark.nettra
@pytest.mark.security
@pytest.mark.functional
@pytest.mark.parametrize(
    "headers_override",
    [
        {"Authorization": "Bearer invalid.token.value"},
        {"Authorization": None},  # sin token
    ],
)
def test_get_well_anomalies_auth_errors(
    nettra_client,
    existing_well_with_anomalies,
    headers_override,
):
    response = nettra_client.get_well_anomalies(
        existing_well_with_anomalies,
        headers_override=headers_override
    )

    assert response.status_code == 401