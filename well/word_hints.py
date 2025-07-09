"""Defines the WordHints class."""

# Standard Imports
from enum import IntEnum
# Third Party Imports
# Local Imports
from well.globals import INPUT_GREEN, INPUT_SKIP, INPUT_YELLOW
from well.letter_hints import LetterHints



class LetterIndex(IntEnum):
    FIRST = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3
    FIFTH = 4

class WordHints():
    """Established facts about a single Wordle word."""

    def __init__(self):
        """WordHints() ctor."""
        self.first = LetterHints()
        self.second = LetterHints()
        self.third = LetterHints()
        self.fourth = LetterHints()
        self.fifth = LetterHints()
        self.word = [self.first, self.second, self.third, self.fourth, self.fifth]
        self._indices = [LetterIndex.FIRST, LetterIndex.SECOND, LetterIndex.THIRD,
                         LetterIndex.FOURTH, LetterIndex.FIFTH]

    def exclude_letter(self, letter: str, skip: LetterIndex = None) -> None:
        """Add an excluded letter to all letters except the skip index."""
        for index in self._indices:
            if index != skip:
                self.word[index].exclude_letter(letter=letter)

    def solve_it(self, letter: str, solved: LetterIndex) -> None:
        """Solve one letter in the word."""
        self.word[solved].solve_it(letter=letter)  # Update the solved letter
        # self.exclude_letter(letter=letter, skip=solved)  # Exclude it from the other letters

    def update_word(self, word: str, results: str) -> None:
        """Update the word based on user feedback."""
        # INPUT VALIDATION
        self._validate_string(five_letters=word, param_name='word')
        self._validate_string(five_letters=results, param_name='results')

        # UPDATE IT
        for index in self._indices:
            # Validate results value
            if INPUT_SKIP == results[index]:
                self.exclude_letter(letter=word[index])
            elif INPUT_YELLOW == results[index]:
                self.word[index].exclude_letter(letter=word[index])
            elif INPUT_GREEN == results[index]:
                self.solve_it(letter=word[index], solved=index)
            else:
                raise ValueError(f'Invalid results entry detected: {results[index]}')

    def _validate_string(self, five_letters: str, param_name: str) -> None:
        """Common use validation functionality."""
        if not isinstance(five_letters, str):
            raise TypeError(f'"{param_name}" must be a string instead of a {type(five_letters)}')
        if 5 != len(five_letters):
            raise ValueError(f'"{param_name}" is not five characters long!')
