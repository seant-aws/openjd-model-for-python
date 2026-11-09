# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

from typing import Any

import pytest

from openjd.model._bool_coercion import _coerce_bool_value


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(2, r"^BOOL value as an integer must be 0 or 1, got 2\.$", id="int"),
        pytest.param(-1, r"^BOOL value as an integer must be 0 or 1, got -1\.$", id="negative-int"),
        pytest.param(0.5, r"^BOOL value as a float must be 0\.0 or 1\.0, got 0\.5\.$", id="float"),
        pytest.param(
            "maybe",
            r"^BOOL value as a string must be one of \(case-insensitive\): "
            r"true, false, yes, no, on, off, 1, 0; got 'maybe'\.$",
            id="string",
        ),
        pytest.param(
            "",
            r"^BOOL value as a string must be one of \(case-insensitive\): "
            r"true, false, yes, no, on, off, 1, 0; got ''\.$",
            id="empty-string",
        ),
        pytest.param(
            None,
            r"^BOOL value must be a boolean, 0/1, 0\.0/1\.0, or a boolean string, got NoneType\.$",
            id="none",
        ),
        pytest.param(
            [True],
            r"^BOOL value must be a boolean, 0/1, 0\.0/1\.0, or a boolean string, got list\.$",
            id="list",
        ),
    ],
)
def test_coerce_bool_value_error_names_the_rejected_value(value: Any, expected: str) -> None:
    with pytest.raises(ValueError, match=expected):
        _coerce_bool_value(value)


@pytest.mark.parametrize(
    "value,expected",
    [
        pytest.param(True, True, id="true"),
        pytest.param(False, False, id="false"),
        pytest.param(1, True, id="int-1"),
        pytest.param(0, False, id="int-0"),
        pytest.param(1.0, True, id="float-1"),
        pytest.param(0.0, False, id="float-0"),
        pytest.param("YES", True, id="upper-yes"),
        pytest.param("Off", False, id="mixed-off"),
    ],
)
def test_coerce_bool_value_accepts_the_spec_spellings(value: Any, expected: bool) -> None:
    assert _coerce_bool_value(value) is expected
