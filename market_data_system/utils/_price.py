from decimal import Decimal


def value_to_decimal_class(value: float | str | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    elif isinstance(value, (int, float)):
        return Decimal.from_float(value)
    elif isinstance(value, str):
        return Decimal(value)
    else:
        raise ValueError(f"Invalid value type: {type(value)}")

