from api.clients.base_client import BaseClient
from typing import Optional, Dict, Any


class NettraClient(BaseClient):

    def get_well_anomalies(
        self,
        well_id: str,
        params: Optional[Dict[str, Any]] = None,
        headers_override: Optional[Dict[str, str]] = None,
    ):
        return self.get(
            f"/wells/{well_id}/anomalies",
            params=params,
            headers_override=headers_override
        )


    def get_well_parameters(
        self,
        well_id: str,
        params: Optional[Dict[str, Any]] = None,
        headers_override: Optional[Dict[str, str]] = None,
    ):
        return self.get(
            f"/wells/{well_id}/parameters",
            params=params,
            headers_override=headers_override
        )