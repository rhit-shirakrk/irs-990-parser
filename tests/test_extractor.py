"""
Tests downloading and extracting information from IRS files
"""

import pytest

from irs990_parser import extractor


class TestIRSExtractor:
    """
    Tests the IRSExtractor class
    """

    def test_downloaded_file_is_not_zip_file_expected_unsupported_file_format_error(
        self,
    ):
        """
        Tests if a downloaded file is a zip file
        """
        sample_url = (
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_01A.zip"
        )
        irs_extractor = extractor.IRSExtractor()
        with pytest.raises(UnsupportedFileError) as excinfo:
            irs_extractor.extract_zip(sample_url)
        assert f"URL {sample_url} does not yield a ZIP file" in str(excinfo)
