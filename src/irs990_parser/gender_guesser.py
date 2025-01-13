import pathlib

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
        prob = self._gender_df[self._gender_df[GenderGuesser.NAME_COL] == first_name][
            GenderGuesser.PROB_COL
        ].values[0]
        return "F" if prob >= 0.5 else "M"
