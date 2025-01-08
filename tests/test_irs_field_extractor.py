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

    def test_ein_extractor_expected_742050021(self) -> None:
        """Tests for proper extraction of an existing EIN field"""
        file_with_ein_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "ein", "contains_ein.xml"
            )
        )
        with open(file_with_ein_path, "r", encoding="utf-8") as f:
            file = f.read()
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ein_extractor = irs_field_extractor.EINEXtractor(
                os.path.basename(file_with_ein_path), parsed_xml
            )
            assert ein_extractor.extract() == "742050021"

    def test_ein_extractor_expected_missing_filer_error(self) -> None:
        """Tests for an error when the Filer section is missing from an IRS form"""
        file_without_filer_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "ein", "missing_filer.xml"
            )
        )
        with open(file_without_filer_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(file_without_filer_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ein_extractor = irs_field_extractor.EINEXtractor(file_name, parsed_xml)
            with pytest.raises(custom_exceptions.MissingFilerException) as excinfo:
                ein_extractor.extract()
            assert f"Filer section missing from file {file_name}" in str(excinfo)

    def test_ein_extractor_expected_missing_ein_error(self) -> None:
        """Tests for an error when an EIN is missing from an IRS form"""
        file_without_ein_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "ein", "missing_ein.xml"
            )
        )
        with open(file_without_ein_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(file_without_ein_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ein_extractor = irs_field_extractor.EINEXtractor(file_name, parsed_xml)
            with pytest.raises(custom_exceptions.MissingEINException) as excinfo:
                ein_extractor.extract()
            assert f"EIN missing from file {file_name}" in str(excinfo)

    def test_org_name_extractor_one_line_field_expected_HABITAT_FOR_HUMANITY_OF_METRO_DENVER(
        self,
    ) -> None:
        """Tests for extracting an organization's name which only uses one line in the form"""
        org_name_extractor = irs_field_extractor.OrgNameExtractor(file_name, parsed_xml)
