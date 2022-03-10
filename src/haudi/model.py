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
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def __available_keys(self):
        annotations = vars(self.__class__).get("__annotations", {}).keys()

    def __field_is_available(self, keys):
        # Implement better code
        return all([key in self.__available_keys for key in keys])

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
