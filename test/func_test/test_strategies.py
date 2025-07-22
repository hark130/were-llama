"""Functionally test WELL strategies.

    Typical usage example:

    python -m test                                       # Run all the test cases
    python -m test.func_test                             # Run all the functional test cases
    python -m test.func_test.test_strategies             # Run all of these test cases
    python -m unittest test.func_test.test_strategies.\
SpecialTestStrategies.test_s01_unique_first_errors       # Run this s01
    python -m unittest test.func_test.test_strategies.\
NormalTestStrategies.test_n04_start_weight_10_percent    # Run this n04
"""

# Standard Imports
from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from enum import auto, IntEnum
from typing import List
from unittest import skip
import os
import sys
# Third Party Imports
from test.func_test.misc import get_commit_hash, get_timestamp
from test.func_test.mocked import get_mocked_feedback
from tediousstart.tediousstart import execute_test_cases, TediousStart
# Local Imports
from well.globals import FIVE_LETTER_WORDS
from well.word_hints import WordHints
from well.words import calc_word_ordict, remove_word_hints
from well.strategy import determine_dupe_weight


@dataclass
class TestCaseStats:
    """Test case statistics."""
    num_guesses: int     # Total number of guesses to get the solution
    solved: bool         # Solved it
    rem_words_1: int     # Number of valid guesses left after Round 1
    error: bool = False  # Communicate an internal error (e.g., 0 guesses left) for logging)


@dataclass
class TotalTestStats:
    """Total test case statistics."""
    total_inputs: int       # Total number of test inputs
    total_guesses: int      # Total number of guesses to get the solution
    total_solved: int       # Solved it
    total_rem_words_1: int  # Number of valid guesses left after Round 1
    total_errors: int       # Communicate an internal error (e.g., 0 guesses left) for logging)


class TestStrategies(TediousStart):
    """WERE LLAMA (WELL) Strategy test class."""

    # CORE CLASS METHODS
    # Methods listed in call order
    def __init__(self, *args, **kwargs) -> None:
        """TestStrategies ctor."""
        super().__init__(*args, **kwargs)
        self.test_start_weight = 1.0  # Test case start weight
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
    def set_start_weight(self, start_weight: float):
        """Convert the TestStrategy enum to a start_weight float value."""
        # INPUT VALIDATION
        self._validate_type(validate_this=start_weight, param_name='start_weight', param_type=float)

        # SET IT
        self.test_start_weight = start_weight

    def log_stderr(self, msg: str) -> None:
        """Log an error to stderr without failing the test case."""
        print(self._test_error.format(str(msg)), file=sys.stderr)

    def log_stats(self, total_stats: TotalTestStats, errors: List[str]) -> None:
        """Process the statistics, print them, and log them."""
        # LOCAL VARIABLES
        test_name = self.id().split('.')[-1]                        # Test case name
        test_stop = get_timestamp()                                 # Stop the timer
        commit_hash = get_commit_hash()                             # Top commit hash
        error_str = '\n' + '\n'.join(errors) if errors else 'None'  # Dynamically build error string
        # Log filename
        log_name = os.path.join(self.test_out,
                                'test_strategies-' + test_name + '-' + test_stop + '.txt')
        # Format string for the log entry
        log_entry = f"""
TEST START: {self._test_start}
    Commit Hash: {commit_hash}
    Total Inputs: {total_stats.total_inputs}
    Avg Solved: {total_stats.total_solved / total_stats.total_inputs * 100:.3f}%
    Avg Guesses: {total_stats.total_guesses / total_stats.total_inputs:.3f}
    Avg Remaining Guesses (Round 1): {total_stats.total_rem_words_1 / total_stats.total_inputs:.3f}
    Num Errors: {total_stats.total_errors}
    ERRORS: {error_str}
TEST STOP:  {test_stop}
        \n"""

        # LOG IT
        # Print it
        print(log_entry)
        with open(log_name, 'w', encoding=sys.getdefaultencoding()) as out_file:
            out_file.write(log_entry)
        print(f'Log saved to: {log_name}')

# pylint: disable=too-many-locals
# Leave me be, Pylint.  It's just test code...
    def replicate_main(self, source: List[str], wordle: str) -> TestCaseStats:
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
        word_hints = WordHints()               # WordHints() object
        available_list = deepcopy(source)      # A deep copy of the source list
        num_guesses = 0                        # TestCaseStats.num_guesses
        solved = False                         # TestCaseStats.solved
        rem_words_1 = 0                        # TestCaseStats.rem_words_1
        error = False                          # TestCaseStats.error
        round_num = 1                          # Keep track of the round
        tmp_ord_dict = OrderedDict()           # Temp OrderedDict from calc_word_ordict()
        tmp_guess = ''                         # Top guess from temp_ord_dict
        tmp_result = ''                        # Mocked user feedback results
        unique = True                          # calc_word_ordict() argument
        start_weight = self.test_start_weight  # The start_weight value for this test case
        dupe_weight = start_weight             # The current dupe_weight value for this test case

        # INPUT VALIDATION
        if wordle.lower() != wordle:
            wordle = wordle.lower()
        if wordle not in source:
            self.fail_test_case(f'Unable to find "{wordle}" in source!')

        # REPLICATE IT
        while True:
            try:
                dupe_weight = determine_dupe_weight(word_hint=word_hints, start_weight=start_weight)
                tmp_ord_dict = calc_word_ordict(available_list, dupe_weight=dupe_weight)
                if tmp_ord_dict:
                    if 2 == round_num:
                        rem_words_1 = len(tmp_ord_dict)  # Store it ASAP, before the "feedback"
                    tmp_guess = list(tmp_ord_dict.keys())[0]
                    tmp_result = get_mocked_feedback(tmp_guess, wordle)
                    num_guesses += 1
                    if tmp_guess == wordle:
                        solved = True
                        break  # Guessed it!
                    word_hints.update_word(tmp_guess, tmp_result)
                    available_list = remove_word_hints(available_list, word_hints)
                else:
                    error = True  # No more guesses but it's not solved?!
                    break  # No need to keep guessing because there's no more guesses available
            except (IndexError, RuntimeError, TypeError, ValueError) as err:
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
# pylint: enable=too-many-locals

    def run_test(self, source: List[str]) -> None:
        """Execute the test case.

        This test class will be doing "How many licks to get to the center of a tootsie pop?"
        trials between different strategies.

        Args:
            source: The list of words to test both with and against.
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
            temp_stats = self.replicate_main(source=FIVE_LETTER_WORDS, wordle=word_input)
            total_guesses += temp_stats.num_guesses
            if temp_stats.solved:
                total_solved += 1
            total_rem_words_1 += temp_stats.rem_words_1
            if temp_stats.error:
                total_errors += 1
                error_list.append(f'Strategy {strategy} encountered an error for '
                                  f'Wordle "{word_input}"')

        # 3. Log the results/stats
        self.log_stats(TotalTestStats(total_inputs=len(source),
                                      total_guesses=total_guesses,
                                      total_solved=total_solved,
                                      total_rem_words_1=total_rem_words_1,
                                      total_errors=total_errors),
                       errors=error_list)


class NormalTestStrategies(TestStrategies):
    """Normal Test Cases."""

    @skip('This test was broken on WELL-4 during a refactor')
    def test_n01_unique_false(self):
        """calc_word_ordict(unique=False)."""
        strategy = TestStrategy.UNIQUE_FALSE  # calc_word_ordict(unique=False)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    @skip('This test was broken on WELL-4 during a refactor')
    def test_n02_unique_first(self):
        """calc_word_ordict(unique=True) on Round 1 only."""
        strategy = TestStrategy.UNIQUE_FIRST  # calc_word_ordict(unique=True) on Round 1 only
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    @skip('This test is causing a plethora of errors... which is fine because it is not viable')
    def test_n03_unique_true(self):
        """calc_word_ordict(unique=True)."""
        strategy = TestStrategy.UNIQUE_TRUE  # calc_word_ordict(unique=True)
        source = FIVE_LETTER_WORDS           # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n04_start_weight_10_percent(self):
        """Start weight value is 10%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.1)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n05_start_weight_20_percent(self):
        """Start weight value is 20%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.2)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n06_start_weight_30_percent(self):
        """Start weight value is 30%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.3)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n07_start_weight_40_percent(self):
        """Start weight value is 40%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.4)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n08_start_weight_50_percent(self):
        """Start weight value is 50%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.5)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n09_start_weight_60_percent(self):
        """Start weight value is 60%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.6)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n10_start_weight_70_percent(self):
        """Start weight value is 70%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.7)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n11_start_weight_80_percent(self):
        """Start weight value is 80%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.8)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n12_start_weight_90_percent(self):
        """Start weight value is 90%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.9)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n13_start_weight_100_percent(self):
        """Start weight value is 100%."""
        source = FIVE_LETTER_WORDS               # Starting list of 5-letter words
        self.set_start_weight(start_weight=1.0)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n14_start_weight_45_percent(self):
        """Start weight value is 45%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.45)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)

    def test_n15_start_weight_55_percent(self):
        """Start weight value is 55%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.55)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n16_start_weight_41_percent(self):
        """Start weight value is 41%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.55)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n17_start_weight_42_percent(self):
        """Start weight value is 42%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.55)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n18_start_weight_43_percent(self):
        """Start weight value is 43%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.55)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n19_start_weight_44_percent(self):
        """Start weight value is 44%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.55)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n20_start_weight_46_percent(self):
        """Start weight value is 46%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.46)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n21_start_weight_47_percent(self):
        """Start weight value is 47%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.47)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n22_start_weight_48_percent(self):
        """Start weight value is 48%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.48)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n23_start_weight_49_percent(self):
        """Start weight value is 49%."""
        source = FIVE_LETTER_WORDS                # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.49)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


    def test_n24_start_weight_45_5_percent(self):
        """Start weight value is 45.5%."""
        source = FIVE_LETTER_WORDS                 # Starting list of 5-letter words
        self.set_start_weight(start_weight=0.455)  # determine_dupe_weight(start_weight)
        self.run_test(source=source)


class ErrorTestStrategies(TestStrategies):
    """Error Test Cases."""


class BoundaryTestTestStrategies(TestStrategies):
    """Boundary Test Cases."""


class SpecialTestStrategies(TestStrategies):
    """Special Test Cases."""

    @skip('This test was broken on WELL-4 during a refactor')
    def test_s01_unique_first_errors(self):
        """Strategy errors from test_n02_unique_first()."""
        strategy = TestStrategy.UNIQUE_FIRST           # calc_word_ordict(unique=True) on Rnd 1 only
        source = ['emery', 'erect', 'every', 'exert']  # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)


if __name__ == '__main__':
    execute_test_cases()
