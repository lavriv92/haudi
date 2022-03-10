import json
from collections import defaultdict

from .utils import isoptional, get_origin_type
from .exceptions import ValidationError
from .fields import RelationField


class ModelMeta(type):
    @property
    def __class_variables(self) -> dict:
        return vars(self)

    def __new__(cls, class_name, bases, attrs):
        instance = super().__new__(cls, class_name, bases, attrs)
        custom_validations = defaultdict(list)

        for field in vars(instance).values():
            field_name = getattr(field, "__validated_field__", None)

            if field_name is not None:
                custom_validations[field_name].append(field)

        instance.__validations__ = custom_validations

        return instance

    @property
    def __field_annotations(self) -> dict:
        return self.__class_variables.get("__annotations__", {})

    def __get_validations(self, field_name):
        return (
            method
            for method in self.__class_variables.values()
            if getattr(method, "__validated_field__", None) == field_name
        )

    def __call__(self, *args, **kwargs):
        errors = defaultdict(list)

        for field_name, annotation in self.__field_annotations.items():
            value = kwargs.get(field_name)

            try:
                if (
                    not isoptional(annotation)
                    and not isinstance(annotation, RelationField)
                    and value is None
                ):
                    raise ValueError(f"{field_name!r} is required")

                if value is None:
                    continue

                origin_type = get_origin_type(annotation)

                if type(value) is not origin_type:
                    raise TypeError(
                        f"Expected value should be {origin_type.__name__!r} but get {type(value).__name__!r}"
                    )

            except (TypeError, ValueError) as e:
                errors[field_name].append(e)
                continue

            for validator in self.__get_validations(field_name):
                try:
                    validator(self, value, *args, **kwargs)
                except ValueError as e:
                    errors[field_name].append(e)
                    continue

        if errors:
            raise ValidationError("Invalid data", error_messages=errors)

        return super().__call__(*args, **kwargs)


class BaseModel(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def dict(self):
        return vars(self)

    @property
    def json(self):
        return json.dumps(self.dict)

    def __setattr__(self, key, value):
        for validator in self.__validations__[key]:
            validator(self, value)

        super().__setattr__(key, value)
