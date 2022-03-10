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


class BaseModel(metaclass=ModelMeta):
    errors: defaultdict = defaultdict(list)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __setattr__(self, key, value):
        for validator in self.__validations__[key]:
            try:
                validator(self, value)
            except (TypeError, ValueError) as e:
                self.errors[key].append(e)
                continue

        super().__setattr__(key, value)

    @property
    def dict(self):
        return vars(self)

    @property
    def json(self):
        return json.dumps(self.dict)

    def save(self):
        if self.errors:
            raise ValidationError("Invalid entity", error_messages=self.errors)
