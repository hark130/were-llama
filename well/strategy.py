"""Implement various WELL strategies."""

# Standard Imports
# Third Party Imports
# Local Imports
from well.globals import DEF_START_WEIGHT
from well.validation import validate_percent, validate_type
from well.word_hints import WordHints


def determine_dupe_weight(word_hint: WordHints, start_weight: float = DEF_START_WEIGHT) -> float:
    """Calculate the dupe_weight value based on current solutions and the starting weight.

    Counts the known letters from word_hint (green and yellow letters).  Then linearly scales
    start_weight to 100% based on the number of known letters.  Floating point values will
    be rounded to the third decimal place to avoid repeating values.
    An example if start_weight is .30:

    | Known | Result |
    ------------------
    | 0     | .30    |
    | 1     | .475   |
    | 2     | .65    |
    | 3     | .825   |
    | 4     | 1.0    |

    Args:
        word_hint: Current state of the game.
        start_weight: Optional; Starting value if word_hint has no known letters.  Must be
            between 0.0 and 1.0, inclusive.
    """
    # LOCAL VARIABLES
    num_known = 0          # Number of known letters in word_hint
    result = start_weight  # Calculated results

    # INPUT VALIDATION
    validate_type(var=word_hint, name='word_hint', var_type=WordHints)
    validate_percent(percent=start_weight, name='start_weight')

    # DETERMINE IT
    num_known = word_hint.count_known()
    if 0 <= num_known < 4:
        result = round(start_weight + ((1.0 - start_weight) * num_known / 4), 3)
    elif num_known in (4, 5):
        result = 1.0
    else:
        raise ValueError(f'Received invalid result from WordHints.count_known(): {num_known}')

    # DONE
    return result
