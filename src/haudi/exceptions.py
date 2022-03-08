class ValidationError(Exception):
    def __init__(self, message, error_messages = {}):
        self.__error_messages = error_messages
        self.message = message

        super().__init__(self.message)

    @property
    def error_messages(self):
        return dict(self.__error_messages)

    @property
    def json(self):
        return { k: [ str(e) for e in v ] for k, v in self.__error_messages.items() }


class InvalidQuery(Exception):
    pass


class RecordNotFound(Exception):
    pass


class UnsupportableLookup(Exception):
    pass


class ModelIsNotExists(Exception):
   pass


class IsNotModel(Exception):
    pass
