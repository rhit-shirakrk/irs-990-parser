"""
Tests all implementations of IRSFieldExtractor
"""

import pathlib

from irs990_parser import irs_field_extractor


class TestIRSFieldExtractor:
    """
    Tests for edge cases in IRS fields
    """

    def test_ein_extractor_expected_381357951(self) -> None:
        """Tests for valid EIN extraction"""
        ein_file = pathlib.Path("sample_irs_xml_files/ein/contains_ein.xml")
        ein_extractor = irs_field_extractor.EINExtractor(ein_file)
