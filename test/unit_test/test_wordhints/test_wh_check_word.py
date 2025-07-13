"""Unit test WordHints.check_word().

    Typical usage example:

    python -m test.unit_test.test_wordhints.test_wh_check_word
"""

# Standard Imports
from collections import namedtuple
from typing import Any, List
# Third Party Imports
from test.unit_test.test_wordhints.test_wordhints import TestWordHints  # Pylint insisted
from tediousstart.tediousstart import execute_test_cases
# Local Imports


# Linked word updates and results as-if read from user input
UserFeedback = namedtuple('UserFeedback', ['word', 'result'])


class TestWordHintsCheckWord(TestWordHints):
    """WordHints().check_word() unit test class."""

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Uses the WordHints() object attribute to call the check_word() method."""
        return self.wh_obj.check_word(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate return value of WordHints.check_word().

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.
        """
        self._validate_return_value(return_value=return_value)

    # HELPER METHODS
    # Methods listed in alphabetical order
    def run_test_fail(self, updates: List[UserFeedback], guess_input: Any,
                      err_type: Exception, err_msg: str = '') -> None:
        """Setup a test case that's expected to fail.

        Args:
            updates: Optional; A list of well-formed input to pass to WordHints().update_word().
                None, or an empty list, will be ignored.
            guess_input: The test case input.
            err_type: Exception type to expect.
            err_msg: Optional; Exception message substring to search for.
        """
        # SETUP
        if updates:
            for update in updates:
                self.call_update_word(update.word, update.result)
        self.set_test_input(guess_input)
        self.expect_exception(err_type, err_msg)

        # RUN IT
        self.run_test()

    def run_test_pass(self, updates: List[UserFeedback], guess_input: str,
                      exp_results: bool) -> None:
        """Setup a test case that's expected to pass.

        Args:
            updates: Optional; A list of well-formed input to pass to WordHints().update_word().
                None, or an empty list, will be ignored.
            guess_input: The test case input.
            exp_results: The expected return value.
        """
        # SETUP
        if updates:
            for update in updates:
                self.call_update_word(update.word, update.result)
        self.set_test_input(guess_input)
        self.expect_return(exp_results)

        # RUN IT
        self.run_test()


class NormalTestWordHintsCheckWord(TestWordHintsCheckWord):
    """Normal Test Cases."""

    def test_n01_round_1(self):
        """New WordHints object."""
        updates = None         # Pre-call input to WordHints().update_word()
        guess_input = 'beans'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n02_round_2_true(self):
        """Round 2 results: guess passes check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('beast', 'gggy ')]  # beans
        guess_input = 'beans'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n03_round_3_true(self):
        """Round 3 results: guess passes check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('below', 'gg   '), UserFeedback('beast', 'gggy ')]  # beans
        guess_input = 'beans'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n04_round_4_true(self):
        """Round 4 results: guess passes check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('zzzzz', '     '), UserFeedback('below', 'gg   '),
                   UserFeedback('beast', 'gggy ')]  # beans
        guess_input = 'beans'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n05_round_5_true(self):
        """Round 5 results: guess passes check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '     '), UserFeedback('qrstu', '  y  '),
                   UserFeedback('beast', 'gggy '), UserFeedback('below', 'gg   ')]  # beans
        guess_input = 'beans'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n06_round_6_true(self):
        """Round 6 results: guess passes check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '     '), UserFeedback('qrstu', '  y  '),
                   UserFeedback('beast', 'gggy '), UserFeedback('below', 'gg   '),
                   UserFeedback('beany', 'gggg ')]  # beans
        guess_input = 'beans'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n07_round_2_false(self):
        """Round 2 results: guess does not pass check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('least', 'g    ')]  # loopy
        guess_input = 'false'  # Test case input
        exp_results = False    # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n08_round_3_false(self):
        """Round 3 results: guess does not pass check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('beast', '     '), UserFeedback('adieu', '     ')]  # loopy
        guess_input = 'false'  # Test case input
        exp_results = False    # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n09_round_4_false(self):
        """Round 4 results: guess does not pass check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('zzzzz', '     '), UserFeedback('lousy', 'ggy g'),
                   UserFeedback('louds', 'gg   ')]  # loopy
        guess_input = 'loops'  # Test case input
        exp_results = False    # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n10_round_5_false(self):
        """Round 5 results: guess does not pass check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy ')]  # loopy
        guess_input = 'floof'  # Test case input
        exp_results = False    # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_n11_round_6_false(self):
        """Round 6 results: guess does not pass check."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('beany', '    g')]  # loopy
        guess_input = 'polly'  # Test case input
        exp_results = False    # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)


class ErrorTestWordHintsCheckWord(TestWordHintsCheckWord):
    """Error Test Cases."""

    def test_e01_bad_type_none(self):
        """The guess argument is None."""
        updates = None       # Pre-call input to WordHints().update_word()
        guess_input = None   # Test case input
        exp_err = TypeError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'must be a string'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)

    def test_e02_bad_type_bytes(self):
        """The guess argument is a byte string."""
        updates = None          # Pre-call input to WordHints().update_word()
        guess_input = b'beans'  # Test case input
        exp_err = TypeError     # Expected exception type
        # Expected exception message substring
        exp_msg = 'must be a string'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)


class BoundaryTestWordHintsCheckWord(TestWordHintsCheckWord):
    """Boundary Test Cases."""

    def test_b01_bad_length_empty(self):
        """The guess argument is empty."""
        updates = None        # Pre-call input to WordHints().update_word()
        guess_input = ''      # Test case input
        exp_err = ValueError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b02_bad_length_one(self):
        """The guess argument is one character long."""
        updates = None        # Pre-call input to WordHints().update_word()
        guess_input = 'b'     # Test case input
        exp_err = ValueError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b03_bad_length_four(self):
        """The guess argument is four characters long."""
        updates = None        # Pre-call input to WordHints().update_word()
        guess_input = 'bean'  # Test case input
        exp_err = ValueError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b04_bad_length_six(self):
        """The guess argument is six characters long."""
        updates = None          # Pre-call input to WordHints().update_word()
        guess_input = 'beeeen'  # Test case input
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b05_bad_length_eleventy_seven(self):
        """The guess argument is eleventy seven characters long."""
        updates = None           # Pre-call input to WordHints().update_word()
        guess_input = 'b' * 117  # Test case input
        exp_err = ValueError     # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(updates=updates, guess_input=guess_input, err_type=exp_err,
                           err_msg=exp_msg)


class SpecialTestWordHintsCheckWord(TestWordHintsCheckWord):
    """Special Test Cases."""

    def test_s01_redundant_answer(self):
        """The user isn't paying attention."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('least', 'g    ')]  # loopy
        guess_input = 'least'  # Test case input
        exp_results = False    # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_s02_legacy_game_test_20250212_round_1(self):
        """Example Wordle #1334."""
        updates = None         # Pre-call input to WordHints().update_word()
        guess_input = 'stein'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_s03_legacy_game_test_20250212_round_2(self):
        """Example Wordle #1334."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('stein', '   g ')]  # ?????
        guess_input = 'radio'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)

    def test_s04_legacy_game_test_20250212_round_3(self):
        """Example Wordle #1334."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('stein', '   g '), UserFeedback('radio', 'ggyg ')]  # ?????
        guess_input = 'rapid'  # Test case input
        exp_results = True     # Expected results
        self.run_test_pass(updates=updates, guess_input=guess_input, exp_results=exp_results)


if __name__ == '__main__':
    execute_test_cases()
