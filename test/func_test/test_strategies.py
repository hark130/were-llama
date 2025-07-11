"""Functionally test WELL strategies.

    Typical usage example:

    python -m test                            # Run all the test cases
    python -m test.func_test                  # Run all the functional test cases
    python -m test.func_test.test_strategies  # Run all of these test cases
"""

# Standard Imports
from collections import OrderedDict, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from enum import auto, IntEnum
from pathlib import Path
from typing import Any, List
import os
import sys
# Third Party Imports
from tediousstart.tediousfunctest import TediousFuncTest
from tediousstart.tediousstart import execute_test_cases, TediousStart
# Local Imports
from well.globals import FIVE_LETTER_WORDS
from well.word_hints import WordHints
from well.words import calc_word_ordict, remove_word_hints
from test.func_test.misc import get_commit_hash, get_timestamp
from test.func_test.mocked import get_mocked_feedback


@dataclass
class TestCaseStats:
    """Test case statistics."""
    num_guesses: int     # Total number of guesses to get the solution
    solved: bool         # Solved it
    rem_words_1: int     # Number of valid guesses left after Round 1
    error: bool = False  # Communicate an internal error (e.g., 0 guesses left) for logging)


class TestStrategy(IntEnum):
    """Communicate the desired test case strategy."""
    UNIQUE_FALSE = auto()  # calc_word_ordict(unique=False)
    UNIQUE_FIRST = auto()  # calc_word_ordict(unique=True) on Round 1 only
    UNIQUE_TRUE = auto()   # calc_word_ordict(unique=True)


class TestStrategies(TediousStart):
    """WERE LLAMA (WELL) Strategy test class."""

    # CORE CLASS METHODS
    # Methods listed in call order
    def __init__(self, *args, **kwargs) -> None:
        """TestStrategies ctor."""
        super().__init__(*args, **kwargs)
        self.test_in = os.path.join(os.getcwd(), 'test', 'func_test', 'test_input')
        self.test_out = os.path.join(os.getcwd(), 'test', 'func_test', 'test_output')
        self._test_start = get_timestamp()

    def setUp(self) -> None:
        """Prepares Test Case.

        Automate any preparation necessary before each Test Case executes.
        """
        super().setUp()
        self._validate_directory(dirname=self.test_in, param_name='test in dir', must_exist=True)
        self._validate_directory(dirname=self.test_out, param_name='test out dir', must_exist=True)

    # HELPER METHODS
    # Methods listed in alphabetical order
    def log_stderr(self, msg: str) -> None:
        """Log an error to stderr without failing the test case."""
        print(self._test_error.format(str(msg)), file=sys.stderr)

    def log_stats(self, num_inputs: int, total_guesses: int, total_solved: int, total_rem_r1: int,
                  total_errors: int, errors: List[str]) -> None:
        """Process the statistics, print them, and log them."""
        # LOCAL VARIABLES
        avg_guesses = '{:.3f}'.format(total_guesses / num_inputs)  # Average guesses
        avg_solved = '{:.3f}'.format(total_solved / num_inputs)    # Average solved
        avg_rem_r1 = '{:.3f}'.format(total_rem_r1 / num_inputs)    # Average words after Rnd 1
        test_name = self.id().split('.')[-1]                       # Test case name
        test_stop = get_timestamp()                                # Stop the timer
        commit_hash = get_commit_hash()                            # Top commit hash
        # Log filename
        log_name = os.path.join(self.test_out,
                                'test_strategies-' + test_name + '-' + test_stop + '.txt')
        # Format string for the log entry
        log_entry = """
TEST START: {start}
    Commit Hash: {commit_hash}
    Total Inputs: {num_inputs}
    Avg Solved: {avg_solved}
    Avg Guesses: {avg_guesses}
    Avg Remaining Guesses (Round 1): {avg_rem_r1}
    Num Errors: {num_errors}
    ERRORS: {error_string}
TEST STOP:  {stop}
        """
        # Formatted log entry
        actual_log_entry = log_entry.format(start=self._test_start, commit_hash=commit_hash,
                                            num_inputs=num_inputs, avg_solved=avg_solved,
                                            avg_guesses=avg_guesses, avg_rem_r1=avg_rem_r1,
                                            num_errors=total_errors,
                                            error_string='\n' + '\n'.join(errors), stop=test_stop)

        # LOG IT
        # Print it
        print(actual_log_entry)
        with open(log_name, 'w') as out_file:
            out_file.write(actual_log_entry)
        print(f'Log saved to: {log_name}')

    def replicate_main(self, source: List[str], wordle: str,
                       strategy: TestStrategy) -> TestCaseStats:
        """Replicate main() by simulating a user always choosing the top answer.

        Args:
            source: Use FIVE_LETTER_WORDS (unless it lags).
            wordle: The actual solution.
            strategy: Controls how well functions are called.

        Returns:
            A TestCaseStats object with the statistics of execution.

        Raises:
            No exception is raised.  The Exception will be printed to stderr and
            TestCaseStats.error will be set to True.
        """
        # LOCAL VARIABLES
        word_hints = WordHints()           # WordHints() object
        available_list = deepcopy(source)  # A deep copy of the source list
        num_guesses = 0                    # TestCaseStats.num_guesses
        solved = False                     # TestCaseStats.solved
        rem_words_1 = 0                    # TestCaseStats.rem_words_1
        error = False                      # TestCaseStats.error
        round_num = 1                      # Keep track of the round
        tmp_ord_dict = OrderedDict()       # Temp OrderedDict from calc_word_ordict()
        tmp_guess = ''                     # Top guess from temp_ord_dict
        tmp_result = ''                    # Mocked user feedback results
        unique = True                      # calc_word_ordict() argument

        # SETUP
        if TestStrategy.UNIQUE_TRUE != strategy and TestStrategy.UNIQUE_FIRST != strategy:
            unique = False  # Only the UNIQUE_TRUE and UNIQUE_FIRST strategies start True

        # INPUT VALIDATION
        if wordle.lower() != wordle:
            wordle = wordle.lower()
        if wordle not in source:
            self.fail_test_case(f'Unable to find "{wordle}" in source!')

        # REPLICATE IT
        while True:
            try:
                if TestStrategy.UNIQUE_FIRST == strategy and round_num != 1:
                    unique = False  # UNIQUE_FIRST only uses unique=True on Round 1
                tmp_ord_dict = calc_word_ordict(available_list, unique=unique)
                if tmp_ord_dict:
                    if 1 == round_num:
                        rem_words_1 = len(tmp_ord_dict)  # Store it ASAP
                    tmp_guess = list(tmp_ord_dict.keys())[0]
                    tmp_result = get_mocked_feedback(tmp_guess, wordle)
                    num_guesses += 1
                    if tmp_guess == wordle:
                        solved = True
                        break  # Guessed it!
                    else:
                        word_hints.update_word(tmp_guess, tmp_result)
                        available_list = remove_word_hints(available_list, word_hints)
                else:
                    error = True  # No more guesses but it's not solved?!
                    break  # No need to keep guessing because there's no more guesses available
            except Exception as err:
                self.log_stderr(f'Encountered an error on round {round_num} for Wordle input '
                                f'"{wordle.upper()}": {repr(err)}')
                error = True
                break  # Stop looping because it will probably happen again
            else:
                round_num += 1  # Increment the round number
                if round_num > 6:
                    break  # Game over, man.  Game over.

        # DONE
        return TestCaseStats(num_guesses=num_guesses, solved=solved,
                             rem_words_1=rem_words_1, error=error)

    def run_test(self, strategy: TestStrategy, source: List[str] = FIVE_LETTER_WORDS) -> None:
        """Execute the test case.

        This test class will be doing "How many licks to get to the center of a tootsie pop?"
        trials between different strategies.

        Args:
            strategy: Controls how well functions are called.
            source: Optional; The list of words to test both with and against.
        """
        # LOCAL VARIABLES
        word_inputs = source   # Test case input
        total_guesses = 0      # Total guesses
        total_solved = 0       # Total games solved (six or less guesses)
        total_rem_words_1 = 0  # Total remaining words after Round 1
        total_errors = 0       # Total errors
        error_list = []        # Error log entries
        temp_stats = None      # Temporary TestCaseStats object

        # 2. For each word
        for word_input in word_inputs:
            temp_stats = self.replicate_main(source=FIVE_LETTER_WORDS, wordle=word_input,
                                             strategy=strategy)
            total_guesses += temp_stats.num_guesses
            if temp_stats.solved:
                total_solved += 1
            total_rem_words_1 += temp_stats.rem_words_1
            if temp_stats.error:
                total_errors += 1
                error_list.append(f'Strategy {strategy} encountered an error for '
                                  f'Wordle "{word_input}"')

        # 3. Log the results/stats
        self.log_stats(num_inputs=len(source), total_guesses=total_guesses,
                       total_solved=total_solved, total_rem_r1=total_rem_words_1,
                       total_errors=total_errors, errors=error_list)


class NormalTestStrategies(TestStrategies):
    """Normal Test Cases."""

    def test_n01_short_unique_false(self):
        """calc_word_ordict(unique=False)."""
        strategy = TestStrategy.UNIQUE_FALSE  # calc_word_ordict(unique=False)
        source = FIVE_LETTER_WORDS[:100]      # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)


class ErrorTestStrategies(TestStrategies):
    """Error Test Cases."""


class BoundaryTestTestStrategies(TestStrategies):
    """Boundary Test Cases."""


class SpecialTestStrategies(TestStrategies):
    """Special Test Cases."""


if __name__ == '__main__':
    execute_test_cases()
