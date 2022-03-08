from typing import get_origin, get_args, Union


def isoptional(annotation):
    return get_origin(annotation) is Union and type(None) in get_args(annotation)


def get_origin_type(annotation):
    if isoptional(annotation):
        origin_type, _ = get_args(annotation)

        return origin_type

    origin_type = get_origin(annotation)

    if origin_type is None:
        return annotation

    return origin_type


def get_tablename(model):
    if hasattr(model, "__tablename__"):
        return model.__tablename__

    return model.__name__
