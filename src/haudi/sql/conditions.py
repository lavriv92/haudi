from .lookups import is_lookup, lookup


def normalize_conditions(conditions: dict):
    normalized_conditions: list = []

    for field, condition in iter(conditions.items()):
        if is_lookup(field):
            normalized_conditions.append(condition)
        else:
            normalized_conditions.append(f"{field}={value}")

    return " AND ".join(normalized_conditions)
