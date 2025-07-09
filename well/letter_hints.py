"""Defines the LetterHints class."""

# Standard Imports
# Third Party Imports
# Local Imports


class LetterHints():
    """Established facts about a single letter in a Wordle word."""

    def __init__(self):
        """LetterHints() ctor."""
        self.solution = ''                                     # Updated when the result is green
        self.excluded = ''                                     # Characters this letter can NOT be
        self._alphabet = 'abcdefghijklmnopqrstuvwxyz'.lower()  # For use during a solution

    def exclude_letter(self, letter: str) -> None:
        """Add an excluded letter.

        Args:
            letter: A single lowercase alphabet character to exclude from these letter hints.
        """
        self._validate_letter(letter)
        if letter not in self.excluded:
            self.excluded = self.excluded + letter

    def is_solved(self) -> bool:
        """Determine if this letter is already solved."""
        # LOCAL VARIABLES
        solved = False  # Die Antwoord

        # IS IT?
        if self.solution:
            solved = True

        # DONE
        return solved

    def solve_it(self, letter: str) -> None:
        """This letter is solved.

        Args:
            letter: A single lowercase alphabet character to solve this letter with.

        Raises:
            RuntimeError: If this letter was already solved.
        """
        if self.is_solved():
            raise RuntimeError('This letter was already solved!')
        self._validate_letter(letter)
        self.excluded = self._alphabet.replace(letter.lower(), '')
        self.solution = letter.lower()

    def _validate_letter(self, letter: str) -> None:
        """Validate one letter.

        Args:
            letter: A single lowercase alphabet character to validate.

        Raise:
            TypeError: Bad type.
            ValueError: Non-lowercase letter, non-alphabet character, or bad string length.
        """
        if not isinstance(letter, str):
            raise TypeError(f'"{letter}" must be a string instead of a {type(letter)}')
        if 1 != len(letter):
            raise ValueError(f'"{letter}" is not a single character!')
        if letter.lower() != letter:
            raise ValueError(f'"letter" must be lower case: {letter}')
        if letter not in self._alphabet:
            raise ValueError(f'"{letter}" is not in the alphabet!')
