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
