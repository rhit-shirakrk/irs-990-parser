"""
Tests loading of data into database
"""

from irs990_parser import irs_field_extractor, loader


class TestLoader:
    """
    Tests functionality of Loader class
    """

    def test_loader_load_organizational_data_model_expected_1(self) -> None:
        """Tests if data is successfully loaded into memory"""
        data_loader = loader.Loader()
        sample_data = irs_field_extractor.OrganizationDataModel(
            ein="1",
            org_name="test",
            year=2024,
            percentage_women_trustees=0.5,
            percentage_women_key_employees=0.3,
            ceo_reviewed_compensation=True,
            other_reviewed_compensation=False,
            male_to_female_pay_ratio=0.2,
            president_to_average_pay_ratio=0.15,
        )
