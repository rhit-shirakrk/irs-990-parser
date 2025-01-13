"""
Tests functionality for guessing gender based off name
"""

import pathlib

from irs990_parser import gender_guesser


class TestGenderGuesser:
    """Tests gender guessing based off name"""

    PROBABILITY_CSV = pathlib.Path(
        "../src/irs990_parser/first_name_gender_probabilities.csv"
    )

    def test_gender_guesser_expected_male(self) -> None:
        """Tests proper guessing of male name"""
        guesser = gender_guesser.GenderGuesser(TestGenderGuesser.PROBABILITY_CSV)
        assert guesser.guess("Brad") == "M"

    def test_gender_guesser_expected_male(self) -> None:
        """Tests proper guessing of male name"""
        guesser = gender_guesser.GenderGuesser(TestGenderGuesser.PROBABILITY_CSV)
        assert guesser.guess("abigail") == "F"

    def test_gender_guesser_unrecognized_name_expected_random(self, mocker) -> None:
        """Tests proper guessing of male name"""
        guesser = gender_guesser.GenderGuesser(TestGenderGuesser.PROBABILITY_CSV)
        mock_random = mocker.patch("random.random")
        mock_random = 0.5
        assert guesser.guess("notinthefile") == "F"
