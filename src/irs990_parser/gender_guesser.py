"""
Guess gender using a probabilities chart
"""

import pathlib
import random

import pandas as pd


class GenderGuesser:
    """
    Guess gender using a probability chart as input

    :param csv_file_path: The file path to a CSV that maps names to probability of being female
    :type csv_file_path: pathlib.Path
    """

    NAME_COL = "Name"
    PROB_COL = "female_prob"

    def __init__(self, csv_file_path: pathlib.Path) -> None:
        self.csv_file_path = csv_file_path
        self._gender_df = pd.read_csv(csv_file_path)
        self._gender_df[GenderGuesser.NAME_COL] = self._gender_df[
            GenderGuesser.NAME_COL
        ].str.lower()
        self._gender_df = self._gender_df.set_index(GenderGuesser.NAME_COL)[
            GenderGuesser.PROB_COL
        ].to_dict()

    def guess(self, first_name: str) -> str:
        """Return guessed gender based off first name

        :param first_name: The first name
        :type first_name: str
        :return: M if male, F if female
        :rtype: str
        """
        first_name = first_name.lower()
        prob = self._gender_df.get(first_name, 0.5)
        return self._guess_using_threshold(prob)

    def _guess_using_threshold(self, threshold: float) -> str:
        """Guess gender based on probability threshold

        :param threshold: Minimum threshold
        :type threshold: float
        :return: M if male, F if female
        :rtype: str
        """
        return "F" if random.random() < threshold else "M"
