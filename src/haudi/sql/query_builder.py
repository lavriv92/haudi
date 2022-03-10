from ..exceptions import InvalidQuery
from ..utils import format_insertion_value
from .conditions import normalize_conditions


class QueryBuilder:
    def __init__(self, model):
        self.__segments = []
        self.model = model

    def query(self, *fields):
        # Implement query

        return self

    def create(self, item):
        keys = ", ".join(item.keys())
        values = ", ".join([format_insertion_value(v) for v in item.values()])

        # Ensure that creation is vorking correnct
        self.__segments.append(
            f"INSERT INTO {self.model.__name__}({keys}) VALUES({values})"
        )

        return self

    def where(self, **conditions):
        if not self.__segments:
            raise InvalidQuery("Query shold not be started from WHERE")

        self.__segments.append(f"WHERE {normalize_conditions(conditions)}")

        return self

    def limit(self, limit_number: int):
        if not self.__segments:
            raise InvalidQuery("Query should not be started from LIMIT")

        self.__segments.append(f"LIMIT {limit}")

        return self

    def skip(self, skip_elements_count: int):
        if not self.__segments:
            raise InvalidQuery("Query should not be started from OFFSET")

        self.__segments.append(f"OFFSET {limit}")

        return self

    def build(self):
        return " ".join(self.__segments)
