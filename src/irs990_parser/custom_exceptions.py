"""
Custom exceptions for parser
"""


class InvalidZipFileException(Exception):
    """
    Thrown when a non-zip file is unexpectedly detected

    :param url: The link to the file
    :type urL: str
    """

    def __init__(self, url: str) -> None:
        super().__init__(f"{url} is not a zip file")
