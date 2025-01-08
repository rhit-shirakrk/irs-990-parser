"""
Implementation of various field extractor classes
"""

import bs4

from irs990_parser import custom_exceptions


class EINEXtractor:
    MISSING_FIELD_MSG = "EIN missing from IRS form"

    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> str:
        """Extract EIN from IRS 990 form

        :return: EIN
        :rtype: str
        """
        filer_xml_object = self.parsed_xml.find("Filer")
        if filer_xml_object is None:
            raise custom_exceptions.MissingFilerException(
                f"Filer section missing from file {self.file_name}"
            )

        ein_xml_object = filer_xml_object.find("EIN")
        if ein_xml_object is None:
            raise custom_exceptions.MissingEINException(
                f"EIN missing from file {self.file_name}"
            )

        return ein_xml_object.text


class OrgNameExtractor:
    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> str:
        """Extract organization name from IRS 990 form

        :return: Organization name
        :rtype: str
        """
        organization_name_xml_object = self.parsed_xml.find("Filer").find(
            "BusinessName"
        )
        if organization_name_xml_object is None:
            raise custom_exceptions.MissingOrganizationNameException(
                f"Organization name missing from file {self.file_name}"
            )
        return " ".join(
            [line.text for line in organization_name_xml_object if line.text != "\n"]
        )
