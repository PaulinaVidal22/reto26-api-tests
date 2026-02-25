from types import MappingProxyType
from copy import deepcopy


class BaseQueryBuilder:
    """
    Builder base para parámetros de query en endpoints GET.
    Devuelve una copia inmutable para evitar efectos colaterales.
    """

    def __init__(self):
        self._params = {}

    def with_date_range(self, from_date: str, to_date: str):
        self._params["from"] = from_date
        self._params["to"] = to_date
        return self

    def with_pagination(self, page: int = 1, page_size: int = 20):
        self._params["page"] = page
        self._params["page_size"] = page_size
        return self

    def build(self):
        """
        Devuelve una copia inmutable de los parámetros
        y resetea el builder para evitar reutilización accidental.
        """
        built = MappingProxyType(deepcopy(self._params))
        self._params.clear()
        return built