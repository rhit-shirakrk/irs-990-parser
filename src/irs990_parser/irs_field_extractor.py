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
        ein_xml_object = self.parsed_xml.find("Filer").find("EIN")
        if ein_xml_object is None:
            raise custom_exceptions.MissingEINException(
                f"EIN missing from file {self.file_name}"
            )
        return ein_xml_object.text
