"""Unit test well.strategy.determine_dupe_weight().

    But why derive from TestWordHints() if we're testing a well.strategy function?
    Because I need the WordHints() test support to inject WordHints() objects into
    the call to determine_dupe_weight().

    Typical usage example:

    python -m test.unit_test.test_wordhints.test_strategy_determine_dupe_weight
"""

# Standard Imports
from collections import namedtuple
from typing import Any, List
# Third Party Imports
from test.unit_test.test_wordhints.test_wordhints import TestWordHints  # Pylint insisted
from tediousstart.tediousstart import execute_test_cases
# Local Imports
from well.letter_hints import LetterHints
from well.strategy import determine_dupe_weight


# Linked word updates and results as-if read from user input
UserFeedback = namedtuple('UserFeedback', ['word', 'result'])


class TestStrategyDetDupeWeight(TestWordHints):
    """WordHints().check_word() unit test class."""

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls determine_dupe_weight()."""
        return determine_dupe_weight(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate return value of WordHints.check_word().

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.
        """
        self._validate_return_value(return_value=return_value)

    # HELPER METHODS
    # Methods listed in alphabetical order
    def run_test_fail(self, updates: List[UserFeedback], start_weight: Any,
                      err_type: Exception, err_msg: str = '') -> None:
        """Setup a test case that's expected to fail.

        Automatically passes in self.wh_obj as word_hint argument value.

        Args:
            updates: Optional; A list of well-formed input to pass to WordHints().update_word().
                None, or an empty list, will be ignored.
            start_weight: The test case input: start_weight.
            err_type: Exception type to expect.
            err_msg: Optional; Exception message substring to search for.
        """
        # SETUP
        if updates:
            for update in updates:
                self.call_update_word(update.word, update.result)
        self.set_test_input(self.wh_obj, start_weight)
        self.expect_exception(err_type, err_msg)

        # RUN IT
        self.run_test()

    def run_test_pass(self, updates: List[UserFeedback],
                      exp_results: bool, start_weight: float = None) -> None:
        """Setup a test case that's expected to pass.

        Automatically passes in self.wh_obj as word_hint argument value.

        Args:
            updates: Optional; A list of well-formed input to pass to WordHints().update_word().
                None, or an empty list, will be ignored.
            exp_results: The expected return value.
            start_weight: Optional; Value to pass in as start_weight.
        """
        # SETUP
        if updates:
            for update in updates:
                self.call_update_word(update.word, update.result)
        if start_weight is not None:
            self.set_test_input(self.wh_obj, start_weight)
        else:
            self.set_test_input(self.wh_obj)
        self.expect_return(exp_results)

        # RUN IT
        self.run_test()


class NormalTestStrategyDetDupeWeight(TestStrategyDetDupeWeight):
    """Normal Test Cases."""

    def test_n01_round_1(self):
        """New WordHints object."""
        updates = None      # Pre-call input to WordHints().update_word()
        start_weight = 0.5  # Test case input: start_weight
        exp_results = 0.5   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n02_round_2(self):
        """Round 2 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('beast', 'gggy ')]  # beans
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n03_round_3(self):
        """Round 3 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('below', 'gg   '), UserFeedback('beast', 'gggy ')]  # beans
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n04_round_4(self):
        """Round 4 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('zzzzz', '     '), UserFeedback('below', 'gg   '),
                   UserFeedback('beast', 'gggy ')]  # beans
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n05_round_5(self):
        """Round 5 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '     '), UserFeedback('qrstu', '  y  '),
                   UserFeedback('beast', 'gggy '), UserFeedback('below', 'gg   ')]  # beans
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n06_round_6(self):
        """Round 6 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '     '), UserFeedback('qrstu', '  y  '),
                   UserFeedback('beast', 'gggy '), UserFeedback('below', 'gg   '),
                   UserFeedback('beany', 'gggg ')]  # beans
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n07_round_2(self):
        """Round 2 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('least', 'g    ')]  # loopy
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.7   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n08_round_3(self):
        """Round 3 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('beast', '     '), UserFeedback('adieu', '     ')]  # loopy
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.6   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n09_round_4(self):
        """Round 4 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('zzzzz', '     '), UserFeedback('lousy', 'gg  g'),
                   UserFeedback('louds', 'gg   ')]  # loopy
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.9   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n10_round_5(self):
        """Round 5 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy ')]  # loopy
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.9   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n11_round_6(self):
        """Round 6 results."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('beany', '    g')]  # loopy
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.9   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n12_docstring_zero(self):
        """Verify the example 'known' in the function docstring: 0."""
        updates = None      # Pre-call input to WordHints().update_word()
        start_weight = 0.3  # Test case input: start_weight
        exp_results = 0.3   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n13_docstring_one(self):
        """Verify the example 'known' in the function docstring: 1."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('ploys', '    g')]  # beans
        start_weight = 0.3   # Test case input: start_weight
        exp_results = 0.475  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n14_docstring_two(self):
        """Verify the example 'known' in the function docstring: 2."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('figgy', 'g  g ')]  # frogs
        start_weight = 0.3  # Test case input: start_weight
        exp_results = 0.65  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n15_docstring_three(self):
        """Verify the example 'known' in the function docstring: 3."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('baahs', 'g g g')]  # beans
        start_weight = 0.3   # Test case input: start_weight
        exp_results = 0.825  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_n15_docstring_four(self):
        """Verify the example 'known' in the function docstring: 4."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('snape', 'yyg y')]  # beans
        start_weight = 0.3  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)


class ErrorTestStrategyDetDupeWeight(TestStrategyDetDupeWeight):
    """Error Test Cases."""

    def test_e01_start_weight_bad_type_none(self):
        """The guess argument is None."""
        updates = None       # Pre-call input to WordHints().update_word()
        start_weight = None  # Test case input: start_weight
        exp_err = TypeError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'must be of type'
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)

    def test_e02_start_weight_bad_type_int(self):
        """The guess argument is a byte string."""
        updates = None       # Pre-call input to WordHints().update_word()
        start_weight = 42    # Test case input: start_weight
        exp_err = TypeError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'must be of type'
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)

    def test_e03_word_hint_bad_type_none(self):
        """The guess argument is None."""
        updates = None       # Pre-call input to WordHints().update_word()
        start_weight = 0.5   # Test case input: start_weight
        exp_err = TypeError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'must be of type'

        self.wh_obj = None  # Set the attribute for this test input
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)

    def test_e04_word_hint_bad_type_letter_hints(self):
        """The guess argument is a byte string."""
        updates = None       # Pre-call input to WordHints().update_word()
        start_weight = 0.2   # Test case input: start_weight
        exp_err = TypeError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'must be of type'

        self.wh_obj = LetterHints()  # Set the attribute for this test input
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)


class BoundaryTestStrategyDetDupeWeight(TestStrategyDetDupeWeight):
    """Boundary Test Cases."""

    def test_b01_start_weight_larg_negative(self):
        """The start_weight argument is a large negative value."""
        updates = None          # Pre-call input to WordHints().update_word()
        start_weight = -90.318  # Test case input: start_weight
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'may not be less than'
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b02_start_weight_barely_negative(self):
        """The start_weight argument is a large negative value."""
        updates = None          # Pre-call input to WordHints().update_word()
        start_weight = -0.0001  # Test case input: start_weight
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'may not be less than'
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b03_start_weight_min(self):
        """The start_weight argument value is barely valid (small)."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('beany', '    g')]  # loopy
        start_weight = 0.0  # Test case input: start_weight
        exp_results = 0.75  # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_b04_start_weight_max(self):
        """The start_weight argument value is barely valid (large)."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('beany', '    g')]  # loopy
        start_weight = 1.0  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_b05_start_weight_barely_too_large(self):
        """The start_weight argument is a large negative value."""
        updates = None          # Pre-call input to WordHints().update_word()
        start_weight = 1.00001  # Test case input: start_weight
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'may not be greater than'
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)

    def test_b06_start_weight_too_large(self):
        """The start_weight argument is a large negative value."""
        updates = None        # Pre-call input to WordHints().update_word()
        start_weight = 100.0  # Test case input: start_weight
        exp_err = ValueError  # Expected exception type
        # Expected exception message substring
        exp_msg = 'may not be greater than'
        self.run_test_fail(updates=updates, start_weight=start_weight, err_type=exp_err,
                           err_msg=exp_msg)


class SpecialTestStrategyDetDupeWeight(TestStrategyDetDupeWeight):
    """Special Test Cases."""

    def test_s01_redundant_answer(self):
        """The user isn't paying attention."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('least', 'g    ')]  # loopy
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.7   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_s02_legacy_game_test_20250212_round_1(self):
        """Example Wordle #1334."""
        updates = None      # Pre-call input to WordHints().update_word()
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.6   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_s03_legacy_game_test_20250212_round_2(self):
        """Example Wordle #1334."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('stein', '   g ')]  # ?????
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 0.7   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_s04_legacy_game_test_20250212_round_3(self):
        """Example Wordle #1334."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('stein', '   g '), UserFeedback('radio', 'ggyg ')]  # ?????
        start_weight = 0.6  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_s05_start_weight_negative_zero(self):
        """The start_weight argument value is a negative zero."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('beany', '    g')]  # loopy
        start_weight = -0.0  # Test case input: start_weight
        exp_results = 0.75   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)

    def test_s06_word_hint_is_solved(self):
        """The word_hint has already been solved."""
        # Pre-call input to WordHints().update_word()
        updates = [UserFeedback('vwxyz', '   y '), UserFeedback('qrstu', '     '),
                   UserFeedback('beast', '     '), UserFeedback('below', '  yy '),
                   UserFeedback('loopy', 'ggggg')]  # loopy
        start_weight = 0.3  # Test case input: start_weight
        exp_results = 1.0   # Expected results
        self.run_test_pass(updates=updates, exp_results=exp_results, start_weight=start_weight)


if __name__ == '__main__':
    execute_test_cases()
