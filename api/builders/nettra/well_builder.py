from api.models.nettra.parameter_models import ParameterResponse
from api.models.nettra.anomaly_models import AnomaliesResponse

class WellBuilder:
    """
    Builder/Selector de wells existentes en entorno QA.
    No crea datos. Solo selecciona wells válidos.
    Implementa:
        - Fluent interface
        - Caching interno
        - Selección desacoplada
    """

    def __init__(self, client, token):
        self.client = client
        self.headers = {"Authorization": f"Bearer {token}"}
        self._wells_cache = None
        self._filters = []

    # =========================
    # Internal helpers
    # =========================

    def _get_all_wells(self):
        if self._wells_cache is not None:
            return self._wells_cache

        response = self.client.get(
            "/wells/",
            headers_override=self.headers
        )

        if response.status_code != 200:
            raise RuntimeError("No se pudieron obtener wells")

        wells = response.json().get("items", [])

        if not wells:
            raise RuntimeError("No existen wells en el entorno")

        self._wells_cache = wells
        return wells

    def _apply_filters(self, wells):
        for filter_func in self._filters:
            wells = filter(filter_func, wells)
        return list(wells)

    # =========================
    # Fluent API
    # =========================

    def with_parameters(self, page_size: int = 50):
        def has_parameters(well):
            response = self.client.get_well_parameters(
                well_id=well["id"],
                params={"page_size": page_size},
                headers_override=self.headers
            )

            if response.status_code != 200:
                return False

            validated = ParameterResponse.model_validate(response.json())
            return bool(validated.data)

        self._filters.append(has_parameters)
        return self

    def with_anomalies(self, page_size: int = 50):
        def has_anomalies(well):
            response = self.client.get_well_anomalies(
                well_id=well["id"],
                params={"page_size": page_size},
                headers_override=self.headers
            )

            if response.status_code != 200:
                return False

            validated = AnomaliesResponse.model_validate(response.json())
            return bool(validated.data)

        self._filters.append(has_anomalies)
        return self

    def any(self):
        wells = self._get_all_wells()
        filtered = self._apply_filters(wells)

        if not filtered:
            return None

        return filtered[0]["id"]