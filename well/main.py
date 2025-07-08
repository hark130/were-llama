"""Entry point for WERE LLAMA (WELL)."""

# Standard Imports
# Third Party Imports
# Local Imports
from well.archive import get_past_answers
from well.globals import FIVE_LETTER_WORDS
from well.words import remove_words


def main() -> int:
    """Entry point for WERE LLAMA (WELL)."""
    # LOCAL VARIABLES
    result = 0  # 0 for success, 1 for failure
    archive_list = None    # List of previous Wordle answers
    available_list = None  # List of available words

    # DO IT
    # 1. Read the archive
    archive_list = get_past_answers()
    # 2. Retrieve dictionary words
    # 3. Remove archive words
    available_list = remove_words(FIVE_LETTER_WORDS, archive_list)
    # 4. Interact
    #   A. Calculate probability of remaining words
    #   B. Take feedback
    #   C. Remove invalid words

    # DONE
    return result
