"""
Implementation of various field extractor classes
"""

from typing import Optional

import bs4
import pydantic

from irs990_parser import custom_exceptions, gender_guesser


class OrganizationDataModel(pydantic.BaseModel):
    ein: str
    instnm: str
    year: int
    percentage_women_trustees: Optional[float]
    percentage_women_key_employees: Optional[float]
    whistleblower_policy: Optional[bool]
    ceo_reviewed_compensation: Optional[bool]
    other_reviewed_compensation: Optional[bool]
    male_to_female_pay_ratio: Optional[float]
    president_to_average_pay_ratio: Optional[float]


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
        try:
            compensation_xml_object = self.parsed_xml.find(
                "CYSalariesCompEmpBnftPaidAmt"
            )
            return float(compensation_xml_object.text)
        except AttributeError:
            return None
        except ValueError:
            return None


class TotalEmployeesExtractor:
    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[int]:
        """Extract number of employees from IRS 990 form

        :return: Number of employees
        :rtype: Optional[int]
        """
        try:
            total_employees_xml_object = self.parsed_xml.find("EmployeeCnt")
            return int(total_employees_xml_object.text)
        except AttributeError:
            return None
        except ValueError:
            return None


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
        try:
            whistleblower_policy_xml_object = self.parsed_xml.find(
                "WhistleblowerPolicyInd"
            )
            return self._implemented_whisteblower_policy(
                whistleblower_policy_xml_object.text
            )
        except AttributeError:
            return None
        except ValueError:
            return None

    def _implemented_whisteblower_policy(self, field_text: str) -> bool:
        if field_text.isdigit():
            return int(field_text) == 1

        return field_text == "true"


class CEOCompensationReviewExtractor:
    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[bool]:
        """Extract CEO compensation review policy from IRS 990 form

        :return: CEO compensation review policy
        :rtype: Optional[bool]
        """
        try:
            ceo_compensation_review_xml_object = self.parsed_xml.find(
                "CompensationProcessCEOInd"
            )
            return self._ceo_reviewed_compensation(
                ceo_compensation_review_xml_object.text
            )
        except AttributeError:
            return None
        except ValueError:
            return None

    def _ceo_reviewed_compensation(self, field_text: str) -> bool:
        if field_text.isdigit():
            return int(field_text) == 1

        return field_text == "true"


class OtherCompensationReviewExtractor:
    PRESENT = 1

    def __init__(self, file_name: str, parsed_xml: bs4.BeautifulSoup) -> None:
        self.file_name = file_name
        self.parsed_xml = parsed_xml

    def extract(self) -> Optional[bool]:
        """Extract Other compensation review policy from IRS 990 form

        :return: Other compensation review policy
        :rtype: Optional[bool]
        """
        try:
            other_compensation_review_xml_object = self.parsed_xml.find(
                "CompensationProcessOtherInd"
            )
            return self._other_reviewed_compensation(
                other_compensation_review_xml_object.text
            )
        except AttributeError:
            return None
        except ValueError:
            return None

    def _other_reviewed_compensation(self, field_text: str) -> bool:
        if field_text.isdigit():
            return int(field_text) == 1
        return field_text == "true"


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

            name_xml_object = trustee_xml_object.find("PersonNm")
            if name_xml_object is None:
                continue

            first_name = name_xml_object.text.split()[0].lower()
            guess = self.guesser.guess(first_name)

            if guess == "F":
                female += 1

            total += 1

        return female / total if total > 0 else None

    def _is_trustee(self, trustee_xml_object: bs4.element.Tag) -> bool:
        """Verify an employee is a trustee

        :param trustee_xml_object: The XML representation of an employee
        :type trustee_xml_object: bs4.element.Tag
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

        :param trustee_xml_object: The XML representation of an employee
        :type trustee_xml_object: bs4.element.Tag
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

        :param trustee_xml_object: The XML representation of an employee
        :type trustee_xml_object: bs4.element.Tag
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

        :param trustee_xml_object: The XML representation of an employee
        :type trustee_xml_object: bs4.element.Tag
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

        :param trustee_xml_object: The XML representation of an employee
        :type trustee_xml_object: bs4.element.Tag
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

    def calculate_key_employee_female_percentage(self) -> Optional[float]:
        """Calculate female percentage of key employees

        :return: Female percentage of key employees
        :rtype: Optional[float]
        """
        schedule_j = self.parsed_xml.find("IRS990ScheduleJ")
        if schedule_j is None:
            return None

        key_employee_xml_objects = schedule_j.find_all("RltdOrgOfficerTrstKeyEmplGrp")

        female = 0
        total = 0
        for key_employee_xml_object in key_employee_xml_objects:
            name = self._get_name_to_guess(key_employee_xml_object)
            if name is None:
                continue

            if self.guesser.guess(name) == "F":
                female += 1
            total += 1

        return female / total if total > 0 else None

    def _get_name_to_guess(
        self, key_employee_xml_object: bs4.element.Tag
    ) -> Optional[str]:
        """Return the name used to guess gender

        :param key_employee_xml_object: XML reprsentation of an employee
        :type key_employee_xml_object: bs4.element.Tag
        :return: The name used to guess gender
        :rtype: Optional[str]
        """
        name_xml_object = key_employee_xml_object.find("PersonNm")
        if name_xml_object is None:
            return None

        full_name = name_xml_object.text.lower().split()
        return full_name[0] if len(full_name) == 2 else full_name[1]

    def calculate_male_to_female_pay_ratio(self) -> Optional[float]:
        """Calculate male to female pay ratio of key employees

        :return: Ratio of male to female pay
        :rtype: float
        """
        schedule_j = self.parsed_xml.find("IRS990ScheduleJ")
        if schedule_j is None:
            return None

        key_employee_xml_objects = schedule_j.find_all("RltdOrgOfficerTrstKeyEmplGrp")
        if key_employee_xml_objects is None:
            return None

        male_pay = 0
        female_pay = 0
        for key_employee_xml_object in key_employee_xml_objects:
            try:
                compensation = float(
                    key_employee_xml_object.find("TotalCompensationFilingOrgAmt").text
                )
                if (
                    self.guesser.guess(self._get_name_to_guess(key_employee_xml_object))
                    == "F"
                ):
                    female_pay += compensation
                else:
                    male_pay += compensation

            except AttributeError:
                continue
            except ValueError:
                continue

        return male_pay / female_pay if female_pay > 0 else None

    def calculate_president_to_average_pay_ratio(self) -> Optional[float]:
        """Calculate president (highest salary) to average wage ratio

        :return: Highest salary to average wage ratio
        :rtype: Optional[float]
        """
        highest_key_employee_salary = self._get_highest_key_employee_salary()
        if highest_key_employee_salary is None:
            return None

        average_salary = self._calculate_average_salary()
        if average_salary is None:
            return None

        return (
            highest_key_employee_salary / average_salary if average_salary > 0 else None
        )

    def _get_highest_key_employee_salary(self) -> Optional[float]:
        """Get highest salary of key employees

        :return: Highest salary
        :rtype: Optional[float]
        """
        schedule_j = self.parsed_xml.find("IRS990ScheduleJ")
        if schedule_j is None:
            return None

        key_employee_xml_objects = schedule_j.find_all("RltdOrgOfficerTrstKeyEmplGrp")
        if key_employee_xml_objects is None:
            return None

        max_pay = 0
        for key_employee_xml_object in key_employee_xml_objects:
            try:
                compensation = float(
                    key_employee_xml_object.find("TotalCompensationFilingOrgAmt").text
                )
                max_pay = max(max_pay, compensation)
            except AttributeError:
                continue
            except ValueError:
                continue

        return max_pay

    def _calculate_average_salary(self) -> Optional[float]:
        """Calculate the average salary of employees in an organization

        :return: Average salary
        :rtype: Optional[float]
        """
        total_salary = float(self.parsed_xml.find("CYSalariesCompEmpBnftPaidAmt").text)
        if total_salary is None:
            return None

        total_salary_of_key_employees = self._calculate_total_salary_of_key_employees()
        if total_salary_of_key_employees is None:
            return None

        total_employee_count_xml_object = self.parsed_xml.find("EmployeeCnt")
        if total_employee_count_xml_object is None:
            return None
        total_employees = int(total_employee_count_xml_object.text)
        total_key_employees = self._get_total_key_employees()

        return (
            (total_salary - total_salary_of_key_employees)
            / (total_employees - total_key_employees)
            if (total_employees - total_key_employees) > 0
            else None
        )

    def _calculate_total_salary_of_key_employees(self) -> Optional[float]:
        """Calculate total salary of all key employees

        :return: Total salary of all key employees
        :rtype: Optional[float]
        """
        schedule_j = self.parsed_xml.find("IRS990ScheduleJ")
        if schedule_j is None:
            return None

        key_employee_xml_objects = schedule_j.find_all("RltdOrgOfficerTrstKeyEmplGrp")
        if key_employee_xml_objects is None:
            return None

        total_salary = 0
        for key_employee_xml_object in key_employee_xml_objects:
            try:
                compensation = float(
                    key_employee_xml_object.find("TotalCompensationFilingOrgAmt").text
                )
                total_salary += compensation
            except AttributeError:
                continue
            except ValueError:
                continue

        return total_salary

    def _get_total_key_employees(self) -> int:
        """Return the number of total key employees

        :return: Number of key employees
        :rtype: int
        """
        schedule_j = self.parsed_xml.find("IRS990ScheduleJ")
        if schedule_j is None:
            return 0

        key_employee_xml_objects = schedule_j.find_all("RltdOrgOfficerTrstKeyEmplGrp")
        if key_employee_xml_objects is None:
            return 0

        return len(key_employee_xml_objects)
