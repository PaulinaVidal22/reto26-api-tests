class AnomaliesQueryBuilder:
    def __init__(self):
        self._params = {}

    def with_date_range(self, from_date: str, to_date: str):
        self._params["from"] = from_date
        self._params["to"] = to_date
        return self

    def with_pagination(self, page: int, page_size: int):
        self._params["page"] = page
        self._params["page_size"] = page_size
        return self

    def build(self):
        return self._params