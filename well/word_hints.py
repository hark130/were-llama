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
        self._must_haves = ''  # Yellow letters that haven't found a home yet

    def check_word(self, guess: str) -> bool:
        """Determine if guess is valid given these word hints.

        Args:
            guess: Lowercase, 5 letter word to evaluate against the current hints.

        Returns:
            True if valid, False otherwise.
        """
        # LOCAL VARIABLES
        valid = True

        # INPUT VALIDATION
        self._validate_string(five_letters=guess, param_name='guess')

        # CHECK IT
        # if guess == 'ghost':
            # print(f'check_word() GHOST!!!!!!!!!!!!!!!!!!!!!!1')  # DEBUGGING
        # Is it excluded anywhere?
        valid = self._check_word_exclusion(guess=guess)
        # Is there room?
        if valid:
            valid = self._check_word_room(guess=guess)
        # Are the "must haves" in the guess?
        if valid:
            valid = self._check_word_must_haves(guess=guess)

        # DONE
        return valid

    def exclude_letter(self, letter: str, skip: LetterIndex = None) -> None:
        """Add an excluded letter to all letters except the skip index.

        Args:
            letter: A single lowercase letter to add to the exclusions.
            skip: Optional; Index of a letter to skip when adding exclusions.
        """
        for index in self._indices:
            if index != skip:
                self.word[index].exclude_letter(letter=letter)

    def solve_it(self, letter: str, solved: LetterIndex) -> None:
        """Solve one letter in the word."""
        self.word[solved].solve_it(letter=letter.lower())  # Update the solved letter
        if letter.lower() in self._must_haves:
            self._must_haves = self._must_haves.replace(letter.lower(), '')

    def update_word(self, word: str, results: str) -> None:
        """Update the word based on user feedback."""
        # INPUT VALIDATION
        self._validate_string(five_letters=word, param_name='word')
        self._validate_string(five_letters=results, param_name='results')

        # UPDATE IT
        for index in self._indices:
            # Validate results value
            if INPUT_SKIP == results[index]:
                if word[index] in self._must_haves:
                    # It has to be somewhere else... but just not here
                    self.word[index].exclude_letter(letter=word[index])
                else:
                    self.exclude_letter(letter=word[index])
            elif INPUT_YELLOW == results[index]:
                self.word[index].exclude_letter(letter=word[index])
                if word[index] not in self._must_haves:
                    self._must_haves = self._must_haves + word[index]
            elif INPUT_GREEN == results[index]:
                self.solve_it(letter=word[index], solved=index)
            else:
                raise ValueError(f'Invalid results entry detected: {results[index]}')

    def _check_word_exclusion(self, guess: str) -> bool:
        """Checks for letter exclusions."""
        # LOCAL VARIABLES
        valid = True

        # CHECK IT
        # Is it excluded anywhere?
        for index in self._indices:
            if guess[index] in self.word[index].excluded:
                # print(f'GUESS {guess[index]} FOUND IN EXCLUSION: {self.word[index].excluded}')  # DEBUGGING
                valid = False  # Not a valid guess
                break

        # DONE
        # print(f'WORD EXCLUSION RETURNS {valid} FOR {guess}')  # DEBUGGING
        return valid

    def _check_word_must_haves(self, guess: str) -> bool:
        """Verify the guess includes all the 'must haves'."""
        # LOCAL VARIABLES
        valid = True  # Prove this wrong

        # CHECK IT
        for must_have in self._must_haves:
            if must_have not in guess:
                valid = False
                break

        # DONE
        # print(f'WORD MUST HAVES RETURNS {valid} FOR {guess}')  # DEBUGGING
        return valid

    def _check_word_room(self, guess: str) -> bool:
        """Checks if there's room in this word for the guess."""
        # LOCAL VARIABLES
        valid = True         # Prove this wrong
        curr_solutions = ''  # Solutions collated from LetterHints()
        local_guess = guess  # Local copy of guess
        # print(f'CHECKING GUESS: {guess}')  # DEBUGGING

        # CHECK IT
        # Check solutions
        for word in self.word:
            curr_solutions = curr_solutions + word.solution
            if word.solution in local_guess:
                local_guess = local_guess.replace(word.solution, '')  # Remove it from the guess
        # Check must haves
        for must_have in self._must_haves:
            if must_have in local_guess:
                local_guess = local_guess.replace(must_have, '')  # Remove it from the guess
        # Check the measurements
        # print(f'MUST HAVES: {self._must_haves}\nLOCAL GUESS: {local_guess}\nCURRENT SOLUTIONS: {curr_solutions}')  # DEBUGGING
        if (len(self._must_haves) + len(local_guess) + len(curr_solutions)) > 5:
            valid = False  # There's just no room

        # DONE
        # print(f'WORD ROOM RETURNS {valid} FOR {guess}')  # DEBUGGING
        return valid

    def _validate_string(self, five_letters: str, param_name: str) -> None:
        """Common use validation functionality.

        Raise:
            TypeError: Bad type.
            ValueError: Non-lowercase word, or bad string length.
        """
        if not isinstance(five_letters, str):
            raise TypeError(f'"{param_name}" must be a string instead of a {type(five_letters)}')
        if 5 != len(five_letters):
            raise ValueError(f'"{param_name}" is not five characters long!')
        if five_letters.lower() != five_letters:
            raise ValueError(f'"{param_name}" must be all lower case: {five_letters}')
