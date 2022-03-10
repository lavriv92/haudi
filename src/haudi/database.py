import sqlite3
from contextlib import contextmanager
from abc import ABC, abstractmethod


class BaseEngine(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def select(self):
        pass


class Sqlite3(BaseEngine):
    def __init__(self, uri):
        self.uri = uri

    def connect(self):
        self.connection = sqlite3.connect(self.uri)
        return self.connection()

    def add(self):
        pass

    def select(self):
        pass

    def close(self):
        self.connection.close()


ENGINES = {"sqlite3": Sqlite3}


class Database:
    def __init__(self, engine: BaseEngine):
        self.__engine = engine

    @contextmanager
    def connection(self):
        try:
            yield self.__engine.connect()
        finally:
            self.__engine.close()


def create_database(uri: str):
    engine_name, _ = uri.split("://")
    engine_class = ENGINES.get(engine_name)

    if not engine_class:
        # TODO: update to library defined error
        raise Exception("Engine is not supported")

    engine = engine_class(uri)

    return Database(engine)
