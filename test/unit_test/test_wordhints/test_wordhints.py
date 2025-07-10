"""Base unit test class for WordHints()."""

# Standard Imports
from typing import Any
# Third Party Imports
from tediousstart.tediousunittest import TediousUnitTest
# Local Imports
from well.word_hints import WordHints


class TestWordHints(TediousUnitTest):
    """WordHints() unit test class.

    This class provides base functionality to run NEBS unit tests for WordHints() methods.
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def __init__(self, *args, **kwargs) -> None:
        """TestWordHints ctor.

        TestWordHints constructor.  Initializes attributes after constructing the parent
        object.

        Args:
            args: Arguments to pass to the parent class ctor.
            kwargs: Keyword arguments to pass to the parent class ctor.
        """
        super().__init__(*args, **kwargs)
        self.wh_obj = None  # WordHints() object

    def setUp(self) -> None:
        """Prepares Test Case.

        Automate any preparation necessary before each Test Case executes.
        """
        super().setUp()
        self.setup_wh_object()  # Create the WordHints() object

    def setup_wh_object(self) -> None:
        """Setup the WordHints() object on behalf of call_callable()."""
        self.wh_obj = WordHints()  # WordHints() object

    def call_callable(self) -> Any:
        """Child class defines test case callable.

        This method must be overridden by the child class.  Be sure to use the object
        returned by self.setup_wh_object().

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # self.setup_wh_object()
        # return self.wh_obj.the_method_you_are_testing(*self._args, **self._kwargs)
        raise NotImplementedError(
            self.fail_test_case('The child class must override the call_callable method'))

    def tearDown(self) -> None:
        """Destroy the WordHints() object."""
        super().tearDown()
        self.wh_obj = None

    # HELPER METHODS
    # Methods listed in alphabetical order
    def call_update_word(self, word: str, results: str) -> None:
        """Allow the test author to safely call WordHints().update_word().

        This is not to test update_word().  Rather, calling update_word() is inherently necessary
        to unit test other class methods.  Any Exception raised will result in a test case failure.
        """
        try:
            return self.wh_obj.update_word(word=word, results=results)
        except (RuntimeError, TypeError, ValueError) as err:
            self.fail_test_case(f'WordHints().update_word({word}, {results}) raised: {repr(err)}')
