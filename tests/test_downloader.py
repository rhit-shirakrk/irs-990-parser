"""
Unit tests for downloading IRS 990 files
"""

import pathlib
from datetime import datetime

import pytest

from irs990_parser import constants, downloader


@pytest.fixture(scope="session")
def mock_directory(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """
    Generate mock directory for usage across multiple tests
    """
    return tmp_path_factory.mktemp("mock_directory")


class TestIRS990FileDownload:
    """
    Unit tests for IRS990FileDownloader class
    """

    def test_earlier_than_2018_start_year_expected_value_error(self) -> None:
        """
        Tests for a start year earlier than 2018
        """
        invalid_start_year = constants.EARLIEST_START_YEAR - 1
        with pytest.raises(ValueError) as excinfo:
            downloader.IRS990FileDownloader(invalid_start_year)
        assert (
            f"Invalid start year {invalid_start_year}. The earliest available year is {constants.EARLIEST_START_YEAR}"
            in str(excinfo.value)
        )

    def test_later_than_current_year_start_year_expected_value_error(self) -> None:
        """
        Tests for a start year later than the current year
        """
        current_year = datetime.now().year
        invalid_start_year = current_year + 1
        with pytest.raises(ValueError) as excinfo:
            downloader.IRS990FileDownloader(invalid_start_year)
        assert (
            f"Invalid start year {invalid_start_year}. The latest available year is {current_year}"
            in str(excinfo.value)
        )

    def test_get_link_to_2018_reports_expected_valid(self) -> None:
        """
        Tests if link to 2018 reports is properly fetched
        """
        LINK_2018 = "https://www.irs.gov/charities-non-profits/form-990-series-downloads#collapseCollapsible1711547204262_839017"
        irs_downloader = downloader.IRS990FileDownloader(constants.EARLIEST_START_YEAR)
        assert LINK_2018 == irs_downloader.get_link_to_yearly_reports(
            constants.EARLIEST_START_YEAR
        )
