"""
Download IRS 990 files and save at specified directory
"""

import pathlib


class IRS990FileDownloader:
    def __init__(self, directory: pathlib.Path) -> None:
        self.directory = directory
