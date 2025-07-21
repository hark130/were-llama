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


class TestStrategy(IntEnum):
    """Communicate the desired test case strategy."""
    UNIQUE_FALSE = auto()  # calc_word_ordict(unique=False)                 # OBE WELL-4 Refactor
    UNIQUE_FIRST = auto()  # calc_word_ordict(unique=True) on Round 1 only  # OBE WELL-4 Refactor
    UNIQUE_TRUE = auto()   # calc_word_ordict(unique=True)                  # OBE WELL-4 Refactor
    STRT_WGT_010 = auto()  # determine_dupe_weight(start_weight=0.10)
    STRT_WGT_020 = auto()  # determine_dupe_weight(start_weight=0.20)
    STRT_WGT_030 = auto()  # determine_dupe_weight(start_weight=0.30)
    STRT_WGT_040 = auto()  # determine_dupe_weight(start_weight=0.40)
    STRT_WGT_050 = auto()  # determine_dupe_weight(start_weight=0.50)
    STRT_WGT_060 = auto()  # determine_dupe_weight(start_weight=0.60)
    STRT_WGT_070 = auto()  # determine_dupe_weight(start_weight=0.70)
    STRT_WGT_080 = auto()  # determine_dupe_weight(start_weight=0.80)
    STRT_WGT_090 = auto()  # determine_dupe_weight(start_weight=0.90)
    STRT_WGT_100 = auto()  # determine_dupe_weight(start_weight=1.00)


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
    def convert_start_weight(self, strategy: TestStrategy) -> float:
        """Convert the TestStrategy enum to a start_weight float value."""
        # LOCAL VARIABLES
        start_weight = 1.0  # Converted start_weight

        # INPUT VALIDATION
        self._validate_type(validate_this=strategy, param_name='strategy', param_type=TestStrategy)

        # CONVERT IT
        match strategy:
            case TestStrategy.STRT_WGT_010:
                start_weight = 0.10
            case TestStrategy.STRT_WGT_020:
                start_weight = 0.20
            case TestStrategy.STRT_WGT_030:
                start_weight = 0.30
            case TestStrategy.STRT_WGT_040:
                start_weight = 0.40
            case TestStrategy.STRT_WGT_050:
                start_weight = 0.50
            case TestStrategy.STRT_WGT_060:
                start_weight = 0.60
            case TestStrategy.STRT_WGT_070:
                start_weight = 0.70
            case TestStrategy.STRT_WGT_080:
                start_weight = 0.80
            case TestStrategy.STRT_WGT_090:
                start_weight = 0.90

        # DONE
        return start_weight

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
        start_weight = 1.0                 # The start_weight value for this test case
        dupe_weight = start_weight         # The current dupe_weight value for this test case

        # SETUP
        if strategy in (TestStrategy.UNIQUE_FALSE, TestStrategy.UNIQUE_FIRST,
                        TestStrategy.UNIQUE_TRUE):
            self.fail_test_case('Unsupported strategy')
        start_weight = self.convert_start_weight(strategy)

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
                    if 1 == round_num:
                        rem_words_1 = len(tmp_ord_dict)  # Store it ASAP
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

    def run_test(self, strategy: TestStrategy, source: List[str]) -> None:
        """Execute the test case.

        This test class will be doing "How many licks to get to the center of a tootsie pop?"
        trials between different strategies.

        Args:
            strategy: Controls how well functions are called.
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
        strategy = TestStrategy.STRT_WGT_010  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n05_start_weight_20_percent(self):
        """Start weight value is 20%."""
        strategy = TestStrategy.STRT_WGT_020  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n06_start_weight_30_percent(self):
        """Start weight value is 30%."""
        strategy = TestStrategy.STRT_WGT_030  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n07_start_weight_40_percent(self):
        """Start weight value is 40%."""
        strategy = TestStrategy.STRT_WGT_040  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n08_start_weight_50_percent(self):
        """Start weight value is 50%."""
        strategy = TestStrategy.STRT_WGT_050  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n09_start_weight_60_percent(self):
        """Start weight value is 60%."""
        strategy = TestStrategy.STRT_WGT_060  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n10_start_weight_70_percent(self):
        """Start weight value is 70%."""
        strategy = TestStrategy.STRT_WGT_070  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n11_start_weight_80_percent(self):
        """Start weight value is 80%."""
        strategy = TestStrategy.STRT_WGT_080  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n12_start_weight_90_percent(self):
        """Start weight value is 90%."""
        strategy = TestStrategy.STRT_WGT_090  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)

    def test_n13_start_weight_100_percent(self):
        """Start weight value is 100%."""
        strategy = TestStrategy.STRT_WGT_100  # determine_dupe_weight(start_weight)
        source = FIVE_LETTER_WORDS            # Starting list of 5-letter words
        self.run_test(strategy=strategy, source=source)


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
