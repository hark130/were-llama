"""Parse word lists."""

# Standard Imports
from typing import List
# Third Party Imports
# Local Imports


def remove_words(source: List[str], remove: List[str]) -> List[str]:
    """Remove words from a master list.

    Args:
        source: A list of words.
        remove: Words to remove from source.

    Returns:
        The new list of source words missing the remove words.
    """
    new_remove = [word.lower() for word in remove]
    return [word.lower() for word in source if word.lower() not in new_remove]
