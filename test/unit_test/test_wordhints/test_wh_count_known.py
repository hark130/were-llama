"""Unit test WordHints.count_known().

    Typical usage example:

    python -m test.unit_test.test_wordhints.test_wh_count_known
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


class TestWordHintsCountKnown(TestWordHints):
    """WordHints().count_known() unit test class."""

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Uses the WordHints() object attribute to call the count_known() method."""
        return self.wh_obj.count_known(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate return value of WordHints.count_known().

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.
        """
        self._validate_return_value(return_value=return_value)

    # HELPER METHODS
    # Methods listed in alphabetical order
    def run_test_fail(self, updates: List[UserFeedback], err_type: Exception,
                      err_msg: str = '') -> None:
        """Setup a test case that's expected to fail.

        Args:
            updates: Optional; A list of well-formed input to pass to WordHints().update_word().
                None, or an empty list, will be ignored.
            err_type: Exception type to expect.
            err_msg: Optional; Exception message substring to search for.
        """
        # SETUP
        if updates:
            for update in updates:
                self.call_update_word(update.word, update.result)
        self.set_test_input()
        self.expect_exception(err_type, err_msg)

        # RUN IT
        self.run_test()

    def run_test_pass(self, updates: List[UserFeedback], exp_results: int) -> None:
        """Setup a test case that's expected to pass.

        Args:
            updates: Optional; A list of well-formed input to pass to WordHints().update_word().
                None, or an empty list, will be ignored.
            exp_results: The expected return value.
        """
        # SETUP
        if updates:
            for update in updates:
                self.call_update_word(update.word, update.result)
        self.set_test_input()
        self.expect_return(exp_results)

        # RUN IT
        self.run_test()


class NormalTestWordHintsCountKnown(TestWordHintsCountKnown):
    """Normal Test Cases."""

    def test_n01_round_1(self):
        """New WordHints object."""
        updates = None   # Pre-call input to WordHints().update_word()
        exp_results = 0  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n02_round_2(self):
        """Round 2 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('beast', 'gggy ')]  # beans
        exp_results = 4  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n03_round_3(self):
        """Round 3 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('below', 'gg   '), UserFeedback('beast', 'gggy ')]  # beans
        exp_results = 4  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n04_round_4(self):
        """Round 4 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('zzzzz', '     '), UserFeedback('below', 'gg   '),
                   UserFeedback('beast', 'gggy ')]  # beans
        exp_results = 4  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n05_round_5(self):
        """Round 5 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '     '), UserFeedback('qrstu', '  y  '),
                   UserFeedback('beast', 'gggy '), UserFeedback('below', 'gg   ')]  # beans
        exp_results = 4  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n06_round_6(self):
        """Round 6 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '     '), UserFeedback('qrstu', '  y  '),
                   UserFeedback('beast', 'gggy '), UserFeedback('below', 'gg   '),
                   UserFeedback('beany', 'gggg ')]  # beans
        exp_results = 5  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n07_round_2(self):
        """Round 2 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('least', 'g    ')]  # loopy
        exp_results = 1  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n08_round_3(self):
        """Round 3 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('beast', '     '), UserFeedback('adieu', '     ')]  # loopy
        exp_results = 0  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n09_round_4(self):
        """Round 4 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('zzzzz', '     '), UserFeedback('lousy', 'gg  g'),
                   UserFeedback('louds', 'gg   ')]  # loopy
        exp_results = 3  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n10_round_5(self):
        """Round 5 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy ')]  # loopy
        exp_results = 3  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_n11_round_6(self):
        """Round 6 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('beany', '    g')]  # loopy
        exp_results = 3  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)


class SpecialTestWordHintsCountKnown(TestWordHintsCountKnown):
    """Special Test Cases."""

    def test_s01_redundant_answer(self):
        """The user isn't paying attention."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('least', 'g    '), UserFeedback('least', 'g    ')]  # loopy
        exp_results = 1  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_s02_legacy_game_test_20250212_round_1(self):
        """Example Wordle #1334."""
        updates = None         # Pre-call input to WordHints().update_word()
        exp_results = 0  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_s03_legacy_game_test_20250212_round_2(self):
        """Example Wordle #1334."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('stein', '   g ')]  # ?????
        exp_results = 1  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)

    def test_s04_legacy_game_test_20250212_round_3(self):
        """Example Wordle #1334."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('stein', '   g '), UserFeedback('radio', 'ggyg ')]  # ?????
        exp_results = 4  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results)


if __name__ == '__main__':
    execute_test_cases()
