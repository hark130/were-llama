"""Entry point for WERE LLAMA (WELL)."""

# Standard Imports
from collections import OrderedDict
# Third Party Imports
# Local Imports
from well.archive import get_past_answers
from well.globals import FIVE_LETTER_WORDS, INPUT_GREEN
from well.prompt import get_feedback
from well.word_hints import WordHints
from well.words import calc_word_ordict, remove_word_hint, remove_words


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
        print(f'TOP GUESSES ({len(ord_dict)} remaining): {", ".join(list(ord_dict.keys())[:10])}')
        try:
            # B. Take feedback
            (temp_word, temp_result) = get_feedback()
            if temp_result == (INPUT_GREEN * 5):
                print('Congratulations!')
                break  # All done
            word_hint.update_word(temp_word, temp_result)
            # C. Remove invalid words
            available_list = remove_word_hint(available_list, word_hint)
        except (TypeError, ValueError) as err:
            print(f'Bad input encountered: {repr(err)}')
            print('Try again.\n')

    # DONE
    return result
