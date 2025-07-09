"""Functionality to interact with the user."""

# Standard Imports
from typing import Tuple
# Third Party Imports
# Local Imports
from well.globals import INPUT_GREEN, INPUT_SKIP_TITLE, INPUT_YELLOW


def get_feedback() -> Tuple[str, str]:
    """Get feedback from the user: word and colors."""
    # LOCAL VARIABLES
    word = ''    # User-input word
    result = ''  # User-input results

    # GET IT
    # Word
    while True:
        print('What word did you type?')
        word = input()
        if 5 != len(word):
            print(f'Invalid word length: {word}\nTry again!')
            continue
        break  # Got it
    # Result
    while True:
        print(f'What were the results?\n({INPUT_GREEN.upper()} for green, '
              f'{INPUT_YELLOW.upper()} for yellow, {INPUT_SKIP_TITLE.upper()} otherwise)')
        result = input()
        if 5 != len(result):
            print(f'Invalid results: {result}\nTry again!')
            continue
        break  # Got it

    # DONE
    return tuple((word.lower(), result.lower()))
