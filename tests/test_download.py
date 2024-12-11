"""
Unit tests for downloading IRS 990 files
"""


class TestIRS990FileDownload:
    def test_nonexistent_directory(self):
        """
        Tests for a non-existent directory to save IRS 990 files
        """
        downloader = IRS990FileDownloader("BAD_PATH")
