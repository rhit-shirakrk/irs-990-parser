"""
Tests all implementations of IRSFieldExtractor
"""

import os
import pathlib

import bs4
import pytest
import pytest_mock

from irs990_parser import custom_exceptions, gender_guesser, irs_field_extractor


@pytest.fixture(scope="session")
def gender_guesser_singleton() -> gender_guesser.GenderGuesser:
    PROB_CSV_FILE = pathlib.Path(
        os.path.join(
            "..", "src", "irs990_parser", "first_name_gender_probabilities.csv"
        )
    )
    return gender_guesser.GenderGuesser(PROB_CSV_FILE)


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
        one_line_org_name_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "org_name", "one_line_name.xml"
            )
        )
        with open(one_line_org_name_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(one_line_org_name_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            org_name_extractor = irs_field_extractor.OrgNameExtractor(
                file_name, parsed_xml
            )
            assert (
                org_name_extractor.extract() == "HABITAT FOR HUMANITY OF METRO DENVER"
            )

    def test_org_name_extractor_multiple_line_field_expected_HABITAT_FOR_HUMANITY_OF_METRO_DENVER_INC(
        self,
    ) -> None:
        """Tests for extracting an organization's name which only uses one line in the form"""
        multiple_line_org_name_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "org_name",
                "multiple_line_name.xml",
            )
        )
        with open(multiple_line_org_name_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(multiple_line_org_name_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            org_name_extractor = irs_field_extractor.OrgNameExtractor(
                file_name, parsed_xml
            )
            assert (
                org_name_extractor.extract()
                == "HABITAT FOR HUMANITY OF METRO DENVER INC"
            )

    def test_org_name_extractor_missing_name_expected_missing_org_name_error(
        self,
    ) -> None:
        """Tests for an error when an organization name is missing from an IRS form"""
        missing_org_name_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "org_name",
                "missing_name.xml",
            )
        )
        with open(missing_org_name_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_org_name_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            org_name_extractor = irs_field_extractor.OrgNameExtractor(
                file_name, parsed_xml
            )
            with pytest.raises(
                custom_exceptions.MissingOrganizationNameException
            ) as excinfo:
                org_name_extractor.extract()
            assert f"Organization name missing from file {file_name}" in str(excinfo)

    def test_org_name_extractor_missing_filer_expected_missing_filer_error(
        self,
    ) -> None:
        """Tests for an error when the filer section is missing from an IRS form"""
        missing_filer_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "org_name",
                "missing_filer.xml",
            )
        )
        with open(missing_filer_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_filer_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            org_name_extractor = irs_field_extractor.OrgNameExtractor(
                file_name, parsed_xml
            )
            with pytest.raises(custom_exceptions.MissingFilerException) as excinfo:
                org_name_extractor.extract()
            assert f"Filer section missing from file {file_name}" in str(excinfo)

    def test_total_compensation_extractor_expected_122207(self) -> None:
        """Tests for proper extraction of total compensation"""
        total_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "total_compensation",
                "compensation.xml",
            )
        )
        with open(total_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(total_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            total_compensation_extractor = (
                irs_field_extractor.TotalCompensationExtractor(file_name, parsed_xml)
            )
            assert total_compensation_extractor.extract() == 122207.0

    def test_total_compensation_extractor_missing_compensation_field_expected_none(
        self,
    ) -> None:
        """Tests for a null return value when the compensation field is missing"""
        missing_total_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "total_compensation",
                "no_compensation.xml",
            )
        )
        with open(missing_total_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_total_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            total_compensation_extractor = (
                irs_field_extractor.TotalCompensationExtractor(file_name, parsed_xml)
            )
            assert total_compensation_extractor.extract() is None

    def test_total_employees_extractor_expected_38(self) -> None:
        """Tests for proper extraction of total employees"""
        total_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "total_employees",
                "multiple_employees.xml",
            )
        )
        with open(total_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(total_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            total_employees_extractor = irs_field_extractor.TotalEmployeesExtractor(
                file_name, parsed_xml
            )
            assert total_employees_extractor.extract() == 38

    def test_total_employees_extractor_missing_employees_expected_none(
        self,
    ) -> None:
        """Tests for a null return value when the total employees field is missing"""
        missing_employees_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "total_employees",
                "missing_employees.xml",
            )
        )
        with open(missing_employees_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_employees_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            total_employees_extractor = irs_field_extractor.TotalEmployeesExtractor(
                file_name, parsed_xml
            )
            assert total_employees_extractor.extract() is None

    def test_whistleblower_policy_extraction_expected_true(self) -> None:
        """Tests for proper extraction of an implemented whistleblower policy"""
        true_whistleblower_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "whistleblower_policy",
                "true.xml",
            )
        )
        with open(true_whistleblower_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(true_whistleblower_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            whistleblower_policy = irs_field_extractor.WhistleblowerPolicyExtractor(
                file_name, parsed_xml
            )
            assert whistleblower_policy.extract() is True

    def test_whistleblower_policy_extraction_expected_false(self) -> None:
        """Tests for proper extraction of an unimplemented whistleblower policy"""
        false_whistleblower_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "whistleblower_policy",
                "false.xml",
            )
        )
        with open(false_whistleblower_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(false_whistleblower_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            whistleblower_policy = irs_field_extractor.WhistleblowerPolicyExtractor(
                file_name, parsed_xml
            )
            assert whistleblower_policy.extract() is False

    def test_whistleblower_policy_extraction_missing_field_expected_none(self) -> None:
        """Tests for missing whistleblower policy field"""
        missing_whistleblower_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "whistleblower_policy",
                "missing_policy.xml",
            )
        )
        with open(missing_whistleblower_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_whistleblower_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            whistleblower_policy = irs_field_extractor.WhistleblowerPolicyExtractor(
                file_name, parsed_xml
            )
            assert whistleblower_policy.extract() is None

    def test_ceo_compensation_review_extraction_expected_true(self) -> None:
        """Tests for proper extraction of CEO compensation review field"""
        true_ceo_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "compensation_review",
                "ceo",
                "true.xml",
            )
        )
        with open(true_ceo_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(true_ceo_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ceo_compensation_policy = (
                irs_field_extractor.CEOCompensationReviewExtractor(
                    file_name, parsed_xml
                )
            )
            assert ceo_compensation_policy.extract() is True

    def test_ceo_compensation_review_extraction_expected_false(self) -> None:
        """Tests for proper extraction of CEO compensation review field"""
        false_ceo_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "compensation_review",
                "ceo",
                "false.xml",
            )
        )
        with open(false_ceo_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(false_ceo_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ceo_compensation_policy = (
                irs_field_extractor.CEOCompensationReviewExtractor(
                    file_name, parsed_xml
                )
            )
            assert ceo_compensation_policy.extract() is False

    def test_ceo_compensation_review_extraction_missing_field_expected_none(
        self,
    ) -> None:
        """Tests for missing CEO compensation review"""
        missing_ceo_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "compensation_review",
                "ceo",
                "missing.xml",
            )
        )
        with open(missing_ceo_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_ceo_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            ceo_compensation_policy = (
                irs_field_extractor.CEOCompensationReviewExtractor(
                    file_name, parsed_xml
                )
            )
            assert ceo_compensation_policy.extract() is None

    def test_other_compensation_review_extraction_expected_true(self) -> None:
        """Tests for proper extraction of Other compensation review field"""
        true_other_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "compensation_review",
                "other",
                "true.xml",
            )
        )
        with open(true_other_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(true_other_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            other_compensation_policy = (
                irs_field_extractor.OtherCompensationReviewExtractor(
                    file_name, parsed_xml
                )
            )
            assert other_compensation_policy.extract() is True

    def test_other_compensation_review_extraction_expected_false(self) -> None:
        """Tests for proper extraction of Other compensation review field"""
        false_other_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "compensation_review",
                "other",
                "false.xml",
            )
        )
        with open(false_other_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(false_other_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            other_compensation_policy = (
                irs_field_extractor.OtherCompensationReviewExtractor(
                    file_name, parsed_xml
                )
            )
            assert other_compensation_policy.extract() is False

    def test_other_compensation_review_extraction_missing_field_expected_non(
        self,
    ) -> None:
        """Tests for missing Other compensation review field"""
        missing_other_compensation_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "compensation_review",
                "other",
                "missing.xml",
            )
        )
        with open(missing_other_compensation_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_other_compensation_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            other_compensation_policy = (
                irs_field_extractor.OtherCompensationReviewExtractor(
                    file_name, parsed_xml
                )
            )
            assert other_compensation_policy.extract() is None

    def test_trustee_extractor_female_percentage_no_male_expected_1(
        self,
        gender_guesser_singleton: gender_guesser.GenderGuesser,
        mocker: pytest_mock.MockerFixture,
    ) -> None:
        """Tests case where there are no male trustees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        :param mocker: Mock fixture
        :type mocker: pytest_mock.MockerFixture
        """
        no_male_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "trustees", "no_male.xml"
            )
        )
        with open(no_male_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_male_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            mocker.patch(
                "irs990_parser.gender_guesser.GenderGuesser.guess", return_value="F"
            )
            trustee_extractor = irs_field_extractor.TrusteeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert trustee_extractor.calculate_trustee_female_percentage() == 1.0

    def test_trustee_extractor_female_percentage_no_female_expected_zero(
        self,
        gender_guesser_singleton: gender_guesser.GenderGuesser,
        mocker: pytest_mock.MockerFixture,
    ) -> None:
        """Tests case where there are no female trustees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        :param mocker: Mock fixture
        :type mocker: pytest_mock.MockerFixture
        """
        no_female_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "trustees", "no_female.xml"
            )
        )
        with open(no_female_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_female_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            mocker.patch(
                "irs990_parser.gender_guesser.GenderGuesser.guess", return_value="M"
            )
            trustee_extractor = irs_field_extractor.TrusteeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert trustee_extractor.calculate_trustee_female_percentage() == 0.0

    def test_trustee_extractor_female_percentage_no_trustees_expected_none(
        self,
        gender_guesser_singleton: gender_guesser.GenderGuesser,
    ) -> None:
        """Tests case where there are no trustees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        no_trustees_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "trustees", "no_trustees.xml"
            )
        )
        with open(no_trustees_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_trustees_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            trustee_extractor = irs_field_extractor.TrusteeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert trustee_extractor.calculate_trustee_female_percentage() is None

    def test_trustee_extractor_female_percentage_both_expected_half(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there are no key employees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        both_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "trustees",
                "both.xml",
            )
        )
        with open(both_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(both_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            trustee_extractor = irs_field_extractor.TrusteeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert trustee_extractor.calculate_trustee_female_percentage() == 0.5

    def test_trustee_extractor_female_percentage_missing_trustees_section_expected_none(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where Part VII Section A is missing

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        missing_trustees_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "trustees", "missing.xml"
            )
        )
        with open(missing_trustees_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_trustees_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            trustee_extractor = irs_field_extractor.TrusteeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert trustee_extractor.calculate_trustee_female_percentage() is None

    def test_key_employee_extractor_female_percentage_no_male_expected_1(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there are no male key employees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        no_male_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "key_employees", "no_male.xml"
            )
        )
        with open(no_male_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_male_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            key_employee_extractor = irs_field_extractor.KeyEmployeeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert (
                key_employee_extractor.calculate_key_employee_female_percentage() == 1.0
            )

    def test_key_employee_extractor_female_percentage_no_female_expected_zero(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there are no female key employees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        no_female_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "key_employees", "no_female.xml"
            )
        )
        with open(no_female_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_female_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            key_employee_extractor = irs_field_extractor.KeyEmployeeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert (
                key_employee_extractor.calculate_key_employee_female_percentage() == 0.0
            )

    def test_key_employee_extractor_female_percentage_both_expected_half(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there are no key employees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        both_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "key_employees",
                "both.xml",
            )
        )
        with open(both_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(both_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            key_employee_extractor = irs_field_extractor.KeyEmployeeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert (
                key_employee_extractor.calculate_key_employee_female_percentage() == 0.5
            )

    def test_key_employee_extractor_female_percentage_missing_schedule_j_expected_none(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there the key employees section is missing

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        missing_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR,
                "key_employees",
                "missing_schedule_j.xml",
            )
        )
        with open(missing_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(missing_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            key_employee_extractor = irs_field_extractor.KeyEmployeeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert (
                key_employee_extractor.calculate_key_employee_female_percentage()
                is None
            )

    def test_key_employee_extractor_male_to_female_pay_ratio_no_male_expected_151195(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there are no male key employees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        no_male_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "key_employees", "no_male.xml"
            )
        )
        with open(no_male_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_male_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            key_employee_extractor = irs_field_extractor.KeyEmployeeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert key_employee_extractor.calculate_male_to_female_pay_ratio() == 0.0

    def test_key_employee_extractor_male_to_female_pay_ratio_no_female_expected_none(
        self, gender_guesser_singleton: gender_guesser.GenderGuesser
    ) -> None:
        """Tests case where there are no female key employees

        :param gender_guesser_singleton: Gender guesser object
        :type gender_guesser_singleton: gender_guesser.GenderGuesser
        """
        no_female_path = pathlib.Path(
            os.path.join(
                TestIRSFieldExtractor.SAMPLE_FILES_DIR, "key_employees", "no_female.xml"
            )
        )
        with open(no_female_path, "r", encoding="utf-8") as f:
            file = f.read()
            file_name = os.path.basename(no_female_path)
            parsed_xml = bs4.BeautifulSoup(file, "xml")
            key_employee_extractor = irs_field_extractor.KeyEmployeeExtractor(
                file_name, parsed_xml, gender_guesser_singleton
            )
            assert key_employee_extractor.calculate_male_to_female_pay_ratio() is None
