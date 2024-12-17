"""
Unit tests for downloading IRS 990 files
"""

import pathlib

import pytest

from irs990_parser import downloader


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

    def test_nonexistent_directory_expected_not_a_directory_error(self) -> None:
        """
        Tests for a non-existent directory to save IRS 990 files
        """
        NON_EXISTENT_DIRECTORY = pathlib.Path("BAD_PATH")
        with pytest.raises(NotADirectoryError) as excinfo:
            downloader.IRS990FileDownloader(NON_EXISTENT_DIRECTORY)
        assert f"Invalid directory {NON_EXISTENT_DIRECTORY}" in str(excinfo.value)

    def test_earlier_than_2018_start_year_expected_value_error(
        self, mock_directory: pathlib.Path
    ) -> None:
        """
        Tests for a start year earlier than 2018
        """
        INVALID_START_YEAR = 2017
        with pytest.raises(ValueError) as excinfo:
            downloader.IRS990FileDownloader(mock_directory, INVALID_START_YEAR)
        assert (
            f"Invalid start year {INVALID_START_YEAR}. The earliest available year is 2018"
            in str(excinfo.value)
        )
