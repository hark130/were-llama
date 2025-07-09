"""Parse word lists."""

# Standard Imports
from collections import OrderedDict
from typing import Dict, List
# Third Party Imports
# Local Imports
from well.globals import REL_START_FREQ, REL_WORD_FREQ
from well.word_hints import WordHints


class CountError(ValueError):
    """A custom except indicating a count violation in a word."""
    pass


def calc_word(word: str, unique: bool = False) -> int:
    """Calculate the likelihood of a word based on frequency."""
    # LOCAL VARIABLES
    prob = REL_START_FREQ[word[0].lower()]  # Calculated value

    # CALC IT
    for letter in word:
        prob += REL_WORD_FREQ[letter.lower()]
    if unique is True and _is_unique_word(word) is False:
        raise CountError(f'"{word}" is not unique')

    # DONE
    return prob


def calc_word_list(words: List[str], unique: bool = False) -> Dict[str, int]:
    """Calculate likelihood for a list of words based on frequency."""
    # LOCAL VARIABLES
    prob_dict = {}  # Dictionary of likelihood

    # CALC THEM
    for word in words:
        try:
            prob_dict[word.lower()] = calc_word(word, unique)
        except CountError:
            pass  # Skip it

    # DONE
    return prob_dict


def calc_word_ordict(words: List[str], unique: bool = False) -> OrderedDict[str, int]:
    """Calculate likelihood for a list of words into a dict sort by descending probability.

    Args:
        words: A list of five letter words to calculate likelihoods for.
        unique: Optional; If True, will only include words that are comprised of unique letters.
    """
    # LOCAL VARIABLES
    prob_dict = calc_word_list(words, unique)
    ord_dict = OrderedDict(dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)))

    # DONE
    return ord_dict


def remove_word_hints(source: List[str], hints: WordHints) -> List[str]:
    """Remove words from source that are incompatible with the word hints.

    Args:
        source: A list of words.
        hints: The WordHints object to validate words against.

    Returns:
        The new list of source words missing words excluded by the word hints.
    """
    # LOCAL VARIABLES
    new_list = []  # New list of words missing guesses excluded by hints

    # REMOVE IT
    for word in source:
        if hints.check_word(word):
            new_list.append(word)

    # DONE
    return new_list


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


def _is_unique_word(word: str) -> bool:
    """Is word comprised of entirely unique letters?"""
    # LOCAL VARIABLES
    unique = False       # Prove this wrong
    unique_letters = ''  # A collection of unique letters from word

    # IS IT?
    for letter in word:
        if letter not in unique_letters:
            unique_letters += letter
    if word == unique_letters:
        unique = True

    # DONE
    return unique
