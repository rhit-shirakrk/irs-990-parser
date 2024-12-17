"""
Download IRS 990 files and save at specified directory
"""

from datetime import datetime

import bs4
import requests

from irs990_parser import constants


class IRS990FileDownloader:
    def __init__(self, start_year: int) -> None:
        self._validate_start_year(start_year)
        self.start_year = start_year
        self._irs_website_html_elements = self._parse_website()

    def _parse_website(self) -> bs4.BeautifulSoup:
        response = requests.get(
            constants.IRS_URL, timeout=constants.IRS_REQUEST_TIMEOUT_SEC
        )
        return bs4.BeautifulSoup(response.text, "html.parser")

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

    def get_index_csv_links(self) -> list[str | list[str]]:
        """
        Return links to index csv files from the start year onward
        """
        href_elements_by_year = self._irs_website_html_elements.select(
            ".collapsible-item-body > p a"
        )
        furthest_year_back = len(href_elements_by_year) - (
            self.start_year - constants.EARLIEST_START_YEAR
        )

        return [item["href"] for item in href_elements_by_year][:furthest_year_back]

    def get_zip_links(self) -> list[str | list[str]]:
        """
        Return links to zip files from the start year onward
        """
        list_elements_by_year = self._irs_website_html_elements.select(
            ".collapsible-item-body"
        )
        zip_links = []
        for item in list_elements_by_year:
            zip_links.extend(
                [
                    link["href"]
                    for link in item.select("a[href$='.zip']")
                    if self._within_year_range(link["href"])
                ]
            )

        return zip_links

    def _within_year_range(self, link: str) -> bool:
        year_from_link = int(link.split("/")[-2])
        return year_from_link >= self.start_year
