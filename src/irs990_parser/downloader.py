"""
Download IRS 990 files and save at specified directory
"""

from datetime import datetime

from irs990_parser import constants


class IRS990FileDownloader:
    def __init__(self, start_year: int) -> None:
        self._validate_start_year(start_year)
        self.start_year = start_year

    def _validate_start_year(self, start_year: int) -> None:
        """
        Ensure start year is between the earliest available year in IRS and current year
        """
        if start_year < constants.EARLIEST_START_YEAR:
            raise ValueError(
                f"Invalid start year {start_year}. The earliest available year is 2018"
            )

        current_year = datetime.now().year
        if start_year > current_year:
            raise ValueError(
                f"Invalid start year {start_year}. The latest available year is {current_year}"
            )
