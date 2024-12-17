"""
Download IRS 990 files and save at specified directory
"""

import os
import pathlib


class IRS990FileDownloader:
    EARLIEST_START_YEAR = 2018

    def __init__(self, directory: pathlib.Path, start_year: int) -> None:
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"Invalid directory {directory}")
        self.directory = directory

        if start_year < IRS990FileDownloader.EARLIEST_START_YEAR:
            raise ValueError(
                f"Invalid start year {start_year}. The earliest available year is 2018"
            )
        self.start_year = start_year
