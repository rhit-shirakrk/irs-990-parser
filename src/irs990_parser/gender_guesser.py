import pathlib


class GenderGuesser:
    def __init__(self, file_path: pathlib.Path) -> None:
        self.file_path = file_path
