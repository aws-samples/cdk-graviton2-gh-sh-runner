"""Module containing helpers and common functions."""

import decimal


def convert_decimal(obj):
    """
    Convert all whole number decimals in 'obj' to integers and others to floats
    """
    if isinstance(obj, list) or isinstance(obj, set):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj
