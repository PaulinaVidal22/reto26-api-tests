from api.models.nettra.parameter_models import ParameterResponse
from api.models.nettra.anomaly_models import AnomaliesResponse


class WellBuilder:
    """
    Builder para resolver wells existentes que cumplan ciertas condiciones.
    No crea datos. Solo selecciona datos válidos del entorno QA.
    """

    def __init__(self, client, token):
        self.client = client
        self.headers = {"Authorization": f"Bearer {token}"}

    def _get_all_wells(self):
        response = self.client.get(
            "/wells/",
            headers_override=self.headers
        )

        if response.status_code != 200:
            raise RuntimeError("No se pudieron obtener wells")

        wells = response.json().get("items", [])
        if not wells:
            raise RuntimeError("No existen wells en el entorno")

        return wells

    def with_anomalies(self, page_size: int = 50):
        """
        Devuelve un well_id que tenga anomalies cargadas.
        """

        wells = self._get_all_wells()

        for well in wells:
            well_id = well["id"]

            response = self.client.get_well_anomalies(
                well_id=well_id,
                params={"page_size": page_size},
                headers_override=self.headers
            )

            if response.status_code == 200:
                validated = AnomaliesResponse.model_validate(
                    response.json()
                )

                if validated.data:
                    return well_id

        return None

    def with_parameters(self, page_size: int = 50):
        """
        Devuelve un well_id que tenga parameter measurements.
        """

        wells = self._get_all_wells()

        for well in wells:
            well_id = well["id"]

            response = self.client.get_well_parameters(
                well_id=well_id,
                params={"page_size": page_size},
                headers_override=self.headers
            )

            if response.status_code == 200:
                validated = ParameterResponse.model_validate(
                    response.json()
                )

                if validated.data:
                    return well_id

        return None