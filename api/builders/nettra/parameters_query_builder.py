from api.builders.nettra.base_query_builder import BaseQueryBuilder


class ParametersQueryBuilder(BaseQueryBuilder):
    """
    Builder para:
    GET /wells/{well_id}/parameters
    """

    def with_parameter_code(self, code: str):
        self._params["parameter_code"] = code
        return self