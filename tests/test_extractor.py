"""
Tests downloading and extracting information from IRS files
"""

import os
import pathlib

import pytest

from irs990_parser import custom_exceptions, extractor


@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Create a temporary directory used for testing

    :param tmp_path_factory: A temporary path fixture
    :type tmp_path_factory: pytest.TempPathFactory
    :return: A path to the temporary directory
    :rtype: pathlib.Path
    """
    TEMP_DIR_NAME = "temp_dir"
    return tmp_path_factory.mktemp(TEMP_DIR_NAME)


class TestIRSExtractor:
    """
    Tests the IRSExtractor class
    """

    def test_downloaded_file_is_not_zip_file_expected_unsupported_file_format_error(
        self, temp_dir: pathlib.Path
    ) -> None:
        """Tests if a downloaded file is a zip file

        :param temp_dir: The path to a temporary directory
        :ptype temp_dir: pathlib.Path
        """
        sample_url = (
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_01A.zipp"
        )
        irs_extractor = extractor.IRSExtractor()
        with pytest.raises(custom_exceptions.InvalidZipFileException) as excinfo:
            irs_extractor.extract_zip(sample_url, temp_dir)
        assert f"URL {sample_url} does not yield a ZIP file" in str(excinfo)

    def test_download_zip_file_expected_one_file_in_temporary_directory(
        self, temp_dir: pathlib.Path
    ) -> None:
        """Tests if a downloaded zip file is saved into a temporary directory

        :param temp_dir: The path to a temporary directory
        :ptype temp_dir: pathlib.Path
        """
        sample_url = (
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_01A.zip"
        )
        irs_extractor = extractor.IRSExtractor()
        path_to_xml_files = irs_extractor.extract_zip(sample_url, temp_dir)
        assert len(list(temp_dir.iterdir())) == 1
        assert path_to_xml_files == os.path.join(temp_dir, "2024_TEOS_XML_01A")
