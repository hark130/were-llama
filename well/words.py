"""Parse word lists."""

# Standard Imports
from collections import OrderedDict
from typing import Dict, List
from typing import OrderedDict as TypingOrderedDict  # TypeError: 'type' object is not subscriptable
# Third Party Imports
# Local Imports
from well.globals import REL_START_FREQ, REL_WORD_FREQ
from well.validation import validate_percent, validate_word
from well.word_hints import WordHints


def calc_word(word: str, dupe_weight: float = 1.0) -> int:
    """Calculate the likelihood of a word based on frequency.

    Args:
        words: A list of five letter words to calculate likelihoods for.
        dupe_weight: Optional; Weight to apply to words with duplicate letters.  Acceptable ranges
            are 0.0 to 1.0.  1.0 essentially disables this feature.  0.0 essentially skips
            words that contain duplicate letters.
    """
    # LOCAL VARIABLES
    prob = REL_START_FREQ[word[0].lower()]  # Calculated value

    # INPUT VALIDATION
    validate_word(word=word, name='word')  # Length will be validated below
    validate_percent(percent=dupe_weight, name='dupe_weight')

    # CALC IT
    for letter in word:
        prob += REL_WORD_FREQ[letter.lower()]
    if not _is_unique_word(word):
        prob *= dupe_weight

    # DONE
    return prob


def calc_word_list(words: List[str], dupe_weight: float = 1.0) -> Dict[str, int]:
    """Calculate likelihood for a list of words based on frequency.

    Args:
        words: A list of five letter words to calculate likelihoods for.
        dupe_weight: Optional; Weight to apply to words with duplicate letters.  Acceptable ranges
            are 0.0 to 1.0.  1.0 essentially disables this feature.
    """
    # LOCAL VARIABLES
    prob_dict = {}  # Dictionary of likelihood

    # CALC THEM
    for word in words:
        prob_dict[word.lower()] = calc_word(word, dupe_weight)

    # DONE
    return prob_dict


def calc_word_ordict(words: List[str], dupe_weight: float = 1.0) -> TypingOrderedDict[str, int]:
    """Calculate likelihood for a list of words into a dict sort by descending probability.

    Args:
        words: A list of five letter words to calculate likelihoods for.
        dupe_weight: Optional; Weight to apply to words with duplicate letters.  Acceptable ranges
            are 0.0 to 1.0.  1.0 essentially disables this feature.
    """
    # LOCAL VARIABLES
    prob_dict = calc_word_list(words, dupe_weight)
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
