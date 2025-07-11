"""Unit test test.func_test.mocked.get_mocked_feedback().

    Typical usage example:

    python -m test                                                       # Run all the test cases
    python -m test.unit_test                                             # Run all the unit tests
    python -m test.unit_test.test_mocked_get_mocked_feedback             # Run these test cases
    python -m unittest test.unit_test.test_mocked_get_mocked_feedback.\
SpecialTestMockedGetMockedFeedback.test_s09_guess_repeats_wordle_twice   # Run this s09
"""

# Standard Imports
from typing import Any
# Third Party Imports
from test.func_test.mocked import get_mocked_feedback
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousunittest import TediousUnitTest
# Local Imports
from well.globals import INPUT_GREEN, INPUT_YELLOW, INPUT_SKIP


class TestMockedGetMockedFeedback(TediousUnitTest):
    """test.func_test.mocked.get_mocked_feedback() unit test class."""

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Uses the WordHints() object attribute to call the check_word() method."""
        return get_mocked_feedback(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate return value of get_mocked_feedback().

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.
        """
        self._validate_return_value(return_value=return_value)

    # HELPER METHODS
    # Methods listed in alphabetical order
    def format_results(self, exp_results: bool) -> str:
        """Format a human-readable exp_results into a string utilizing the well.globals."""
        # LOCAL VARIABLES
        new_results = exp_results.lower()  # Gotta start somewhere

        # FORMAT IT
        new_results = new_results.replace('g', INPUT_GREEN)
        new_results = new_results.replace(' ', INPUT_SKIP)
        new_results = new_results.replace('y', INPUT_YELLOW)

        # TEST IT
        for letter in new_results:
            if letter not in f'{INPUT_GREEN}{INPUT_SKIP}{INPUT_YELLOW}':
                self.fail_test_case(f'Test author used an unexpected character: {exp_results}')
        if 5 != len(new_results):
            self.fail_test_case('Test author provided an expected result that was not '
                                f'5 characters long: {exp_results}')

        # DONE
        return new_results

    def run_test_fail(self, guess_input: Any, wordle_input: Any,
                      err_type: Exception, err_msg: str = '') -> None:
        """Setup a test case that's expected to fail.

        Args:
            guess_input: The test case input: guess.
            wordle_input: The test case input: wordle.
            err_type: Exception type to expect.
            err_msg: Optional; Exception message substring to search for.
        """
        # SETUP
        self.set_test_input(guess_input, wordle_input)
        self.expect_exception(err_type, err_msg)

        # RUN IT
        self.run_test()

    def run_test_pass(self, guess_input: Any, wordle_input: Any, exp_results: str) -> None:
        """Setup a test case that's expected to pass.

        Args:
            guess_input: The test case input: guess.
            wordle_input: The test case input: wordle.
            exp_results: The expected return value.
        """
        # SETUP
        self.set_test_input(guess_input, wordle_input)
        self.expect_return(exp_results)

        # RUN IT
        self.run_test()


class NormalTestMockedGetMockedFeedback(TestMockedGetMockedFeedback):
    """Normal Test Cases."""

    def test_n01_worst_guess(self):
        """No hits."""
        guess_input = 'frank'                        # Test case input: guess
        wordle_input = 'goopy'                       # Test case input: wordle
        exp_results = self.format_results('     ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_n02_bad_guess(self):
        """One off-position hits."""
        guess_input = 'frank'                        # Test case input: guess
        wordle_input = 'laugh'                       # Test case input: wordle
        exp_results = self.format_results('  y  ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_n03_ok_guess(self):
        """One on and one off hit."""
        guess_input = 'blown'                        # Test case input: guess
        wordle_input = 'beans'                       # Test case input: wordle
        exp_results = self.format_results('g   y')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_n04_good_guess(self):
        """Two on-position hits."""
        guess_input = 'frank'                        # Test case input: guess
        wordle_input = 'beans'                       # Test case input: wordle
        exp_results = self.format_results('  gg ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_n05_great_guess(self):
        """Four on-position hits."""
        guess_input = 'loopy'                        # Test case input: guess
        wordle_input = 'goopy'                       # Test case input: wordle
        exp_results = self.format_results(' gggg')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_n06_best_guess(self):
        """All hits."""
        guess_input = 'beans'                        # Test case input: guess
        wordle_input = 'beans'                       # Test case input: wordle
        exp_results = self.format_results('ggggg')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)


class ErrorTestMockedGetMockedFeedback(TestMockedGetMockedFeedback):
    """Error Test Cases."""

    def test_e01_guess_bad_type_none(self):
        """The guess argument is None."""
        guess_input = None      # Test case input: guess
        wordle_input = 'beans'  # Test case input: wordle
        exp_err = TypeError     # Expected exception type
        # Expected exception message substring
        exp_msg = 'instead received type'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_e02_guess_bad_type_bytes(self):
        """The guess argument is a byte string."""
        guess_input = b'beans'  # Test case input: guess
        wordle_input = 'beans'  # Test case input: wordle
        exp_err = TypeError     # Expected exception type
        # Expected exception message substring
        exp_msg = 'instead received type'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_e03_wordle_bad_type_none(self):
        """The wordle argument is None."""
        guess_input = 'beans'  # Test case input: guess
        wordle_input = None    # Test case input: wordle
        exp_err = TypeError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'instead received type'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_e04_wordle_bad_type_bytes(self):
        """The wordle argument is a byte string."""
        guess_input = 'beans'    # Test case input: guess
        wordle_input = b'beans'  # Test case input: wordle
        exp_err = TypeError      # Expected exception type
        # Expected exception message substring
        exp_msg = 'instead received type'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)


class BoundaryTestMockedGetMockedFeedback(TestMockedGetMockedFeedback):
    """Boundary Test Cases."""

    def test_b01_guess_bad_length_empty(self):
        """The guess argument is empty."""
        guess_input = ''        # Test case input: guess
        wordle_input = 'beans'  # Test case input: wordle
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'can not be empty'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b02_guess_bad_length_one(self):
        """The guess argument is one character long."""
        guess_input = 'b'       # Test case input: guess
        wordle_input = 'beans'  # Test case input: wordle
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b03_guess_bad_length_four(self):
        """The guess argument is four characters long."""
        guess_input = 'bean'    # Test case input: guess
        wordle_input = 'beans'  # Test case input: wordle
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b04_guess_bad_length_six(self):
        """The guess argument is six characters long."""
        guess_input = 'beeeen'  # Test case input: guess
        wordle_input = 'beans'  # Test case input: wordle
        exp_err = ValueError    # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b05_guess_bad_length_eleventy_seven(self):
        """The guess argument is eleventy seven characters long."""
        guess_input = 'b' * 117  # Test case input: guess
        wordle_input = 'beans'   # Test case input: wordle
        exp_err = ValueError     # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b06_wordle_bad_length_empty(self):
        """The wordle argument is empty."""
        guess_input = 'beans'  # Test case input: guess
        wordle_input = ''      # Test case input: wordle
        exp_err = ValueError   # Expected exception type
        # Expected exception message substring
        exp_msg = 'can not be empty'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b07_wordle_bad_length_one(self):
        """The wordle argument is one character long."""
        guess_input = 'beans'  # Test case input: guess
        wordle_input = 'b'     # Test case input: wordle
        exp_err = ValueError   # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b08_wordle_bad_length_four(self):
        """The wordle argument is four characters long."""
        guess_input = 'beans'  # Test case input: guess
        wordle_input = 'bean'  # Test case input: wordle
        exp_err = ValueError   # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b09_wordle_bad_length_six(self):
        """The wordle argument is six characters long."""
        guess_input = 'beans'    # Test case input: guess
        wordle_input = 'beeeen'  # Test case input: wordle
        exp_err = ValueError     # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)

    def test_b10_wordle_bad_length_eleventy_seven(self):
        """The wordle argument is eleventy seven characters long."""
        guess_input = 'beans'     # Test case input: guess
        wordle_input = 'b' * 117  # Test case input: wordle
        exp_err = ValueError      # Expected exception type
        # Expected exception message substring
        exp_msg = 'not five characters long'
        self.run_test_fail(guess_input=guess_input, wordle_input=wordle_input,
                           err_type=exp_err, err_msg=exp_msg)


class SpecialTestMockedGetMockedFeedback(TestMockedGetMockedFeedback):
    """Special Test Cases."""

    def test_s01_wordle_repeats_non_guess(self):
        """Wordle has a repeating letter not in the guess."""
        guess_input = 'beans'                        # Test case input: guess
        wordle_input = 'floof'                       # Test case input: wordle
        exp_results = self.format_results('     ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s02_wordle_repeats_first_guess_letter(self):
        """First guess letter is repeated in the wordle."""
        guess_input = 'frank'                        # Test case input: guess
        wordle_input = 'floof'                       # Test case input: wordle
        exp_results = self.format_results('g    ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s03_wordle_repeats_second_guess_letter(self):
        """Second guess letter is repeated in the wordle."""
        guess_input = 'after'                        # Test case input: guess
        wordle_input = 'floof'                       # Test case input: wordle
        exp_results = self.format_results(' y   ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s04_wordle_repeats_third_guess_letter(self):
        """Third guess letter is repeated in the wordle."""
        guess_input = 'ulfen'                        # Test case input: guess
        wordle_input = 'floof'                       # Test case input: wordle
        exp_results = self.format_results(' gy  ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s05_wordle_repeats_fourth_guess_letter(self):
        """Fourth guess letter is repeated in the wordle."""
        guess_input = 'lords'                        # Test case input: guess
        wordle_input = 'dudes'                       # Test case input: wordle
        exp_results = self.format_results('   yg')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s06_wordle_repeats_fifth_guess_letter(self):
        """Fifth guess letter is repeated in the wordle."""
        guess_input = 'lords'                        # Test case input: guess
        wordle_input = 'sassy'                       # Test case input: wordle
        exp_results = self.format_results('    y')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s07_guess_repeats_wordle_once(self):
        """The guess has a repeating letter found in the wordle once."""
        guess_input = 'bubba'                        # Test case input: guess
        wordle_input = 'beans'                       # Test case input: wordle
        exp_results = self.format_results('g   y')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s08_guess_repeats_wordle_once_second_in_place(self):
        """The guess has a repeating letter, 2nd is in-place, found in the wordle once."""
        guess_input = 'boooh'                        # Test case input: guess
        wordle_input = 'prods'                       # Test case input: wordle
        exp_results = self.format_results('  g  ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s09_guess_repeats_wordle_twice(self):
        """The guess has a repeating letter, 2nd is in-place, found in the wordle once."""
        guess_input = 'boooh'                        # Test case input: guess
        wordle_input = 'foody'                       # Test case input: wordle
        exp_results = self.format_results(' gg  ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)

    def test_s10_what_does_wordle_do_here(self):
        """The guess has a repeating letter found in the wordle once, once in-place and once not.

        ChatGPT says...
        This follows the official New York Times Wordle rules:
        🟩 Green – letter is in the correct position.
        🟨 Yellow – letter is in the word but in the wrong position.
        ⬛ Gray – letter is not in the word at all or has already been accounted for.

        The key for this test case is... "already been accounted for".
        """
        guess_input = 'foody'                        # Test case input: guess
        wordle_input = 'flops'                       # Test case input: wordle
        exp_results = self.format_results('gy   ')   # Expected results
        self.run_test_pass(guess_input=guess_input, wordle_input=wordle_input,
                           exp_results=exp_results)


if __name__ == '__main__':
    execute_test_cases()
