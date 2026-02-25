from api.builders.nettra.base_query_builder import BaseQueryBuilder


class WellsQueryBuilder(BaseQueryBuilder):
    """
    Builder para:
    GET /wells/
    """

    def with_search(self, search: str):
        self._params["search"] = search
        return self