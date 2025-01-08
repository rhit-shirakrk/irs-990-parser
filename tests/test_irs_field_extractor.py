"""
Tests all implementations of IRSFieldExtractor
"""

import os
import pathlib

import bs4
import pytest

from irs990_parser import custom_exceptions, irs_field_extractor


class TestIRSFieldExtractor:
    """
    Tests for edge cases in IRS fields
    """

    SAMPLE_FILES_DIR = pathlib.Path("sample_irs_xml_files/")

    def test_ein_extractor_expected_381357951(self) -> None:
        """Tests for an error when a non-xml file is being parsed"""
        file_with_ein_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "ein", "contains_ein.xml"
            )
        )
        with open(file_with_ein_path, "r", encoding="utf-8") as f:
            file = f.read()
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ein_extractor = irs_field_extractor.EINEXtractor(parsed_xml)
            assert ein_extractor.extract() == 381357951
