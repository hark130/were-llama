"""Entry point for WERE LLAMA (WELL)."""

# Standard Imports
from collections import OrderedDict
# Third Party Imports
# Local Imports
from well.archive import get_past_answers
from well.globals import FIVE_LETTER_WORDS
from well.prompt import get_feedback
from well.word_hints import WordHints
from well.words import calc_word_ordict, remove_words


def main() -> int:
    """Entry point for WERE LLAMA (WELL)."""
    # LOCAL VARIABLES
    result = 0  # 0 for success, 1 for failure
    archive_list = []         # List of previous Wordle answers
    available_list = []       # List of available words
    ord_dict = OrderedDict()  # OrderedDict of word probabilities
    unique = True             # Only display unique solutions on round 1
    word_hint = WordHints()   # WordHints object
    temp_word = ''            # Word input from user
    temp_result = ''          # Results input from user

    # DO IT
    # 1. Read the archive
    archive_list = get_past_answers()
    # 2. Retrieve dictionary words
    # 3. Remove archive words
    available_list = remove_words(FIVE_LETTER_WORDS, archive_list)
    # 4. Interact
    while (True):
        # A. Calculate probability of remaining words
        ord_dict = calc_word_ordict(available_list, unique=unique)
        unique = False
        print(f'TOP TEN: {", ".join(list(ord_dict.keys())[:10])}')
        # B. Take feedback
        (temp_word, temp_result) = get_feedback()
        word_hint.update_word(temp_word, temp_result)
        # C. Remove invalid words

        print(f'FIRST:  {word_hint.first.excluded}')  # DEBUGGING
        print(f'SECOND: {word_hint.second.excluded}')  # DEBUGGING
        print(f'THIRD:  {word_hint.third.excluded}')  # DEBUGGING
        print(f'FOURTH: {word_hint.fourth.excluded}')  # DEBUGGING
        print(f'FIFTH:  {word_hint.fifth.excluded}')  # DEBUGGING
        break  # DEBUGGING

    # DONE
    return result
