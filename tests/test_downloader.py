"""
Unit tests for downloading IRS 990 files
"""

import pathlib

import pytest

from irs990_parser import downloader


class TestIRS990FileDownload:
    def test_nonexistent_directory(self):
        """
        Tests for a non-existent directory to save IRS 990 files
        """
        NON_EXISTENT_DIRECTORY = pathlib.Path("BAD_PATH")
        with pytest.raises(NotADirectoryError) as excinfo:
            file_downloader = downloader.IRS990FileDownloader(NON_EXISTENT_DIRECTORY)
        assert f"Invalid directory {NON_EXISTENT_DIRECTORY}" in str(excinfo.value)
