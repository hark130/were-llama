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
    result = ''   # Mocked feedback
    matches = ''  # Store letters already been accounted for

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
    for index in range(5):
    # for g_char, w_char in zip(guess, wordle):
        g_char = guess[index]
        w_char = wordle[index]
        if g_char == w_char:
            result = result + INPUT_GREEN
            matches = matches + g_char  # Accounted for
        elif g_char in wordle:
            if 1 == wordle.count(g_char):
                result = result + INPUT_YELLOW
                matches = matches + g_char  # Accounted for
            else:
                # Multiple occurences of g_char in the wordle
                print(f'\nGUESS:   {guess}')  # DEBUGGING
                print(f'WORDLE:  {wordle}')  # DEBUGGING
                print(f'MATCHES: {matches}')  # DEBUGGING
                if wordle.count(g_char) == matches.count(g_char):
                    result = result + INPUT_SKIP  # All matches for this letter accounted for
                else:
                    result = result + INPUT_YELLOW
        else:
            result = result + INPUT_SKIP

    # DONE
    return result
