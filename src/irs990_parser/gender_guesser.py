import pathlib
import random

import pandas as pd


class GenderGuesser:
    NAME_COL = "Name"
    PROB_COL = "female_prob"

    def __init__(self, file_path: pathlib.Path) -> None:
        self.file_path = file_path
        self._gender_df = pd.read_csv(file_path)
        self._gender_df[GenderGuesser.NAME_COL] = self._gender_df[
            GenderGuesser.NAME_COL
        ].str.lower()

    def guess(self, first_name: str) -> str:
        """Return guessed gender based off first name

        :param first_name: The first name
        :type first_name: str
        :return: M if male, F if female
        :rtype: str
        """
        first_name = first_name.lower()
        prob_in_df = self._gender_df[
            self._gender_df[GenderGuesser.NAME_COL] == first_name
        ][GenderGuesser.PROB_COL].values
        if prob_in_df.size == 0:
            return self._guess_using_threshold(0.5)

        return self._guess_using_threshold(prob_in_df[0])

    def _guess_using_threshold(self, threshold: float) -> str:
        """Guess gender based on probability threshold

        :param threshold: Minimum threshold
        :type threshold: float
        :return: M if male, F if female
        :rtype: str
        """
        return "F" if random.random() < threshold else "M"
