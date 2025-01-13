import pathlib


class GenderGuesser:
    def __init__(self, file_path: pathlib.Path) -> None:
        self.file_path = file_path

    def guess(self, first_name: str) -> str:
        """Return guessed gender based off first name

        :param first_name: The first name
        :type first_name: str
        :return: M if male, F if female
        :rtype: str
        """
        return "M"
