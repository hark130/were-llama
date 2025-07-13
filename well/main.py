"""Entry point for WERE LLAMA (WELL)."""

# Standard Imports
from collections import OrderedDict
# Third Party Imports
# Local Imports
from well.archive import get_past_answers
from well.globals import FIVE_LETTER_WORDS, INPUT_GREEN
from well.prompt import get_feedback
from well.word_hints import WordHints
from well.words import calc_word_ordict, CountError, remove_word_hints, remove_words


def main() -> int:
    """Entry point for WERE LLAMA (WELL)."""
    # LOCAL VARIABLES
    result = 0  # 0 for success, 1 for failure
    archive_list = []         # List of previous Wordle answers
    available_list = []       # List of available words
    ord_dict = OrderedDict()  # OrderedDict of word probabilities
    unique = False            # EDIT: Disabling "first true unique" strategy
    word_hints = WordHints()  # WordHints object
    temp_word = ''            # Word input from user
    temp_result = ''          # Results input from user

    # DO IT
    # 1. Read the archive
    archive_list = get_past_answers()
    # 2. Retrieve dictionary words
    # 3. Remove archive words
    available_list = remove_words(FIVE_LETTER_WORDS, archive_list)
    # 4. Interact
    while True:
        # A. Calculate probability of remaining words
        ord_dict = calc_word_ordict(available_list, unique=unique)
        if not ord_dict:
            print('Something has gone wrong.  There are no more available guesses.\n'
                  'Perhaps a typo (or a BUG).')
            result = 1
            break  # No more guesses, so no need to continue
        unique = False
        print(f'TOP GUESSES ({len(ord_dict)} remaining): {", ".join(list(ord_dict.keys())[:10])}')
        try:
            # B. Take feedback
            (temp_word, temp_result) = get_feedback()
            if temp_result == (INPUT_GREEN * 5):
                print('Congratulations!')
                break  # All done
            word_hints.update_word(temp_word, temp_result)
            # C. Remove invalid words
            available_list = remove_word_hints(available_list, word_hints)
        except (CountError, RuntimeError) as err:
            print(f'Error encountered: {repr(err)}')
            print('Exiting.\n')
            result = 1
            break
        except (TypeError, ValueError) as err:
            print(f'Bad input encountered: {repr(err)}')
            print('Try again.\n')
        except KeyboardInterrupt:
            print('\nExiting.\n')
            break

    # DONE
    return result
