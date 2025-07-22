"""Common validation functionality."""

# Standard Imports
from typing import Any
# Third Party Imports
# Local Imports


def validate_percent(percent: float, name: str) -> None:
    """Validate a float value as a percent ranging from 0% to 100%, inclusive.

    Args:
        percent: The value to validate.
        name: The name of the argument being validated (for use in Exception messages).

    Raises:
        TypeError: Bad data type.
        ValueError: Bad value.
    """
    validate_type(var=percent, name=name, var_type=float)
    if percent < 0.0:
        raise ValueError(f'"{name}" may not be less than 0.0: {percent}')
    if percent > 1.0:
        raise ValueError(f'"{name}" may not be greater than 1.0: {percent}')


def validate_string(string: str, name: str, can_be_empty: bool = False) -> None:
    """Validate a strings type and content.

    Args:
        string: The string to validate.
        name: The name of the argument being validated (for use in Exception messages).
        can_be_empty: Optional; If True, the string can be empty.

    Raises:
        TypeError: Bad data type.
        ValueError: Bad value.
    """
    validate_type(var=string, name=name, var_type=str)
    if 0 == len(string) and can_be_empty is False:
        raise ValueError(f'"{name}" may not be an empty string')


def validate_type(var: Any, name: str, var_type: type) -> None:
    """Validate var against a data type.

    Args:
        var: The variable to validate.
        name: The name of the argument being validated (for use in Exception messages).
        var_type: The expected variable type.

    Raises:
        TypeError: Bad data type.
        ValueError: Bad value.
    """
    invalid = '"{name}" must be of type "{var_type}" instead of "{wrong_type}"'
    if not isinstance(name, str):
        raise TypeError(invalid.format(name='name', var_type=str, wrong_type=type(name)))
    if not isinstance(var, var_type):
        raise TypeError(invalid.format(name=name, var_type=var_type, wrong_type=type(var)))


def validate_word(word: str, name: str) -> None:
    """Validate word as a five character string.

    Args:
        word: The string to validate as five character word.
        name: The name of the argument being validated (for use in Exception messages).

    Raises:
        TypeError: Bad data type.
        ValueError: Bad value.
    """
    validate_string(string=word, name=name, can_be_empty=True)  # Length will be validated below
    if 5 != len(word):
        raise ValueError(f'"{name}" is not five characters long!')
