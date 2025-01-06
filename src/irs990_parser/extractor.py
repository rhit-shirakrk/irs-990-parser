"""
Download and extract information from IRS files
"""

from irs990_parser import custom_exceptions


class IRSExtractor:
    def __init__(self) -> None:
        pass

    def extract_zip(self, url: str) -> None:
        raise custom_exceptions.InvalidZipFileException(
            f"URL {url} does not yield a ZIP file"
        )
