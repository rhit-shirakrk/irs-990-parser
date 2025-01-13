"""
Implementation of various field extractor classes
"""

from typing import Optional

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
        filer_xml_object = self.parsed_xml.find("Filer")
        if filer_xml_object is None:
            raise custom_exceptions.MissingFilerException(
                f"Filer section missing from file {self.file_name}"
            )

        organization_name_xml_object = filer_xml_object.find("BusinessName")

        if organization_name_xml_object is None:
            raise custom_exceptions.MissingOrganizationNameException(
                f"Organization name missing from file {self.file_name}"
            )
        return " ".join(
            [line.text for line in organization_name_xml_object if line.text != "\n"]
        )


class TotalCompensationExtractor:
    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[float]:
        """Extract total compensation from IRS 990 form

        :return: Total compensation
        :rtype: float
        """
        compensation_xml_object = self.parsed_xml.find("CYSalariesCompEmpBnftPaidAmt")
        if compensation_xml_object is None:
            return None

        return float(compensation_xml_object.text)


class TotalEmployeesExtractor:
    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[int]:
        """Extract number of employees from IRS 990 form

        :return: Number of employees
        :rtype: int
        """
        total_employees_xml_object = self.parsed_xml.find("EmployeeCnt")
        if total_employees_xml_object is None:
            return None

        return int(total_employees_xml_object.text)


class WhistleblowerPolicyExtractor:
    PRESENT = 1

    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[bool]:
        """Extract whistleblower policy from IRS 990 form

        :return: Whether a whistleblower policy is present
        :rtype: bool
        """
        whistleblower_policy_xml_object = self.parsed_xml.find("WhistleblowerPolicyInd")
        if whistleblower_policy_xml_object is None:
            return None

        return self._implemented_whisteblower_policy(
            int(whistleblower_policy_xml_object.text)
        )

    def _implemented_whisteblower_policy(self, checked: int) -> bool:
        return checked == WhistleblowerPolicyExtractor.PRESENT


class CEOCompensationReviewExtractor:
    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml
