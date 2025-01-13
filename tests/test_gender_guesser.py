"""
Tests functionality for guessing gender based off name
"""

import pathlib

import pytest_mock

from irs990_parser import gender_guesser


class TestGenderGuesser:
    """Tests gender guessing based off name"""

    PROBABILITY_CSV = pathlib.Path(
        "../src/irs990_parser/first_name_gender_probabilities.csv"
    )

    def test_gender_guesser_expected_male(self) -> None:
        """Tests proper guessing of male name"""
        guesser = gender_guesser.GenderGuesser(TestGenderGuesser.PROBABILITY_CSV)
        assert guesser.guess("brad") == "M"

    def test_gender_guesser_expected_female(self) -> None:
        """Tests proper guessing of female name"""
        guesser = gender_guesser.GenderGuesser(TestGenderGuesser.PROBABILITY_CSV)
        assert guesser.guess("abigail") == "F"

    def test_gender_guesser_unrecognized_name_expected_random(
        self, mocker: pytest_mock.MockerFixture
    ) -> None:
        """Tests proper guessing of missing name"""
        mocker.patch("random.random", return_value=0.5)

        guesser = gender_guesser.GenderGuesser(TestGenderGuesser.PROBABILITY_CSV)
        assert guesser.guess("notinthefile") == "M"
