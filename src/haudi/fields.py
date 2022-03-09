class RelationField:
    def __init__(self, relation_model):
        self.__value = None
        self.relation_model = relation_model

    def __get__(self, obj, objtype=None):
        return self.__value

    def __set__(self, obj, value):
        self.__value = value
