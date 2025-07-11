"""Mocked functionality on behalf of the test framework."""

# Standard Imports
# Third Party Imports
from hobo.validation import validate_string
# Local Imports
from well.globals import INPUT_GREEN, INPUT_YELLOW, INPUT_SKIP


def get_mocked_feedback(guess: str, wordle: str) -> str:
    """Replicate the behavior of Wordle and replicate well.prompt.get_feedback().

    Args:
        guess: The test case's guess.
        wordle: The actual solution to evaluate guess against.

    Returns:
        A string made up of five characters.  Those characters will be:
            well.globals.INPUT_GREEN
            well.globals.INPUT_YELLOW
            well.globals.INPUT_SKIP
    """
    # LOCAL VARIABLES
    result = ''  # Mocked feedback

    # INPUT VALIDATION
    # guess
    validate_string(guess, 'guess', can_be_empty=False)
    if 5 != len(guess):
        raise ValueError(f'The guess value "{guess}" is not five characters long!')
    # wordle
    validate_string(wordle, 'wordle', can_be_empty=False)
    if 5 != len(wordle):
        raise ValueError(f'The wordle value "{wordle}" is not five characters long!')

    # GET IT
    for g_char, w_char in zip(guess, wordle):
        if g_char == w_char:
            result = result + INPUT_GREEN
        elif g_char in wordle:
            if 1 == wordle.count(g_char):
                result = result + INPUT_YELLOW
            else:
                # Multiple occurences of g_char in the wordle
                # TO DO: DON'T DO NOW... IMPLEMENT THIS LATER
                raise NotImplementedError(f'UNABLE TO HANDLE GUESS "{guess}" FOR WORDLE "{wordle}"')
        else:
            result = result + INPUT_SKIP

    # DONE
    return result
