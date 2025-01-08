"""
Implementation of various field extractor classes
"""

import bs4


class EINEXtractor:
    def __init__(self, parsed_xml: bs4.BeautifulSoup) -> None:
        self.parsed_xml = parsed_xml

    def extract(self) -> str:
        """Extract EIN from IRS 990 form

        :return: EIN
        :rtype: str
        """
        return self.parsed_xml.find("Filer").find("EIN").text
