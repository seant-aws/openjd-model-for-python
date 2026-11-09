# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

from typing import Any

# Accepted string spellings for boolean defaults/values (case-insensitive),
# per RFC 0007 (BOOL parameter type).
_BOOL_TRUE_STRINGS = frozenset({"true", "yes", "on", "1"})
_BOOL_FALSE_STRINGS = frozenset({"false", "no", "off", "0"})


def _coerce_bool_value(value: Any) -> bool:
    """Coerce an RFC 0007 BOOL value to a Python bool, raising ValueError for
    anything outside the accepted set (bool, int 0/1, float 0.0/1.0, or a
    case-insensitive true/false/yes/no/on/off/1/0 string).
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):  # bool already handled above
        if value in (0, 1):
            return bool(value)
        raise ValueError(f"BOOL value as an integer must be 0 or 1, got {value}.")
    if isinstance(value, float):
        if value in (0.0, 1.0):
            return bool(value)
        raise ValueError(f"BOOL value as a float must be 0.0 or 1.0, got {value}.")
    if isinstance(value, str):
        low = value.lower()
        if low in _BOOL_TRUE_STRINGS:
            return True
        if low in _BOOL_FALSE_STRINGS:
            return False
        raise ValueError(
            "BOOL value as a string must be one of (case-insensitive): "
            f"true, false, yes, no, on, off, 1, 0; got {value!r}."
        )
    # Name only the type: the value of an unsupported type (a list, a mapping) can be arbitrarily large.
    raise ValueError(
        "BOOL value must be a boolean, 0/1, 0.0/1.0, or a boolean string, "
        f"got {type(value).__name__}."
    )
