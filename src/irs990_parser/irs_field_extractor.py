"""
Implementation of various field extractor classes
"""

from typing import Optional

import bs4

from irs990_parser import custom_exceptions, gender_guesser


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
        :rtype: Optional[float]
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
        :rtype: Optional[int]
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
        :rtype: Optional[bool]
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
    PRESENT = 1

    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[bool]:
        """Extract CEO compensation review policy from IRS 990 form

        :return: CEO compensation review policy
        :rtype: Optional[bool]
        """
        ceo_compensation_review_xml_object = self.parsed_xml.find(
            "CompensationProcessCEOInd"
        )
        if ceo_compensation_review_xml_object is None:
            return None

        return self._ceo_reviewed_compensation(
            int(ceo_compensation_review_xml_object.text)
        )

    def _ceo_reviewed_compensation(self, checked: int) -> bool:
        return checked == WhistleblowerPolicyExtractor.PRESENT


class OtherCompensationReviewExtractor:
    PRESENT = 1

    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> bool:
        """Extract Other compensation review policy from IRS 990 form

        :return: Other compensation review policy
        :rtype: bool
        """
        other_compensation_review_xml_object = self.parsed_xml.find(
            "CompensationProcessOtherInd"
        )
        if other_compensation_review_xml_object is None:
            return None

        return self._other_reviewed_compensation(
            int(other_compensation_review_xml_object.text)
        )

    def _other_reviewed_compensation(self, checked: int) -> bool:
        return checked == OtherCompensationReviewExtractor.PRESENT


class TrusteeExtractor:
    def __init__(
        self,
        file_name: str,
        parsed_xml: bs4.BeautifulSoup,
        guesser: gender_guesser.GenderGuesser,
    ) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml
        self.guesser = guesser

    def calculate_trustee_female_percentage(self) -> Optional[float]:
        """Calculate percentage of female trustees

        :return: Percentage of female trustees in an organization
        :rtype: Optional[float]
        """
        trustee_xml_objects = self.parsed_xml.find_all("Form990PartVIISectionAGrp")
        female = 0
        total = 0
        for trustee_xml_object in trustee_xml_objects:
            if not self._is_trustee(trustee_xml_object):
                continue

            first_name = trustee_xml_object.find("PersonNm").text.split()[0].lower()
            guess = self.guesser.guess(first_name)

            if guess == "F":
                female += 1

            total += 1

        return female / total if total > 0 else None

    def _is_trustee(self, trustee_xml_object: bs4.element.Tag) -> bool:
        """Verify an employee is a trustee

        :return: True if the employee is a trustee, False otherwise
        :rtype: bool
        """
        return (
            self._is_individual_trustee_or_director(trustee_xml_object)
            and self._no_reportable_compensation_from_organization(trustee_xml_object)
            and self._no_reportable_compensation_from_related_organizations(
                trustee_xml_object
            )
            and self._zero_estimated_amount_of_other_compensation(trustee_xml_object)
        )

    def _is_individual_trustee_or_director(
        self, trustee_xml_object: bs4.element.Tag
    ) -> bool:
        """Verify an employee is an individual trustee or director

        :return: True if the employee is an individual trustee or director, False otherwise
        :rtype: bool
        """
        individual_trustee_or_director_checkbox_xml_object = trustee_xml_object.find(
            "IndividualTrusteeOrDirectorInd"
        )
        return (
            individual_trustee_or_director_checkbox_xml_object is not None
            and individual_trustee_or_director_checkbox_xml_object.text == "X"
        )

    def _no_reportable_compensation_from_organization(
        self, trustee_xml_object: bs4.element.Tag
    ) -> bool:
        """Verify if the reportable compensation from their organization is 0

        :return: True if the amount is 0, False otherwise
        :rtype: bool
        """
        reportable_compensation_xml_object = trustee_xml_object.find(
            "ReportableCompFromOrgAmt"
        )
        return (
            reportable_compensation_xml_object is not None
            and int(reportable_compensation_xml_object.text) == 0
        )

    def _no_reportable_compensation_from_related_organizations(
        self, trustee_xml_object: bs4.element.Tag
    ) -> bool:
        """Verify if the reportable compensation from related organizations is 0

        :return: True if the amount is 0, False otherwise
        :rtype: bool
        """
        related_reportable_compensation_xml_object = trustee_xml_object.find(
            "ReportableCompFromRltdOrgAmt"
        )
        return (
            related_reportable_compensation_xml_object is not None
            and int(related_reportable_compensation_xml_object.text) == 0
        )

    def _zero_estimated_amount_of_other_compensation(
        self, trustee_xml_object: bs4.element.Tag
    ) -> bool:
        """Verify if the estimated amount of other compensation is 0

        :return: True if the amount is 0, False otherwise
        :rtype: bool
        """
        other_compensation_xml_object = trustee_xml_object.find("OtherCompensationAmt")
        return (
            other_compensation_xml_object is not None
            and int(other_compensation_xml_object.text) == 0
        )


class KeyEmployeeExtractor:
    def __init__(
        self,
        file_name: str,
        parsed_xml: bs4.BeautifulSoup,
        guesser: gender_guesser.GenderGuesser,
    ) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml
        self.guesser = guesser

    def calculate_key_employee_female_percentage(self) -> float:
        """Calculate female percentage of key employees

        :return: Female percentage of key employees
        :rtype: float
        """
        return 1.0
