"""
Tests loading of data into database
"""

from irs990_parser import loader


class TestLoader:
    """
    Tests functionality of Loader class
    """

    def test_loader_load_organizational_data_model_expected_1(self) -> None:
        """Tests if data is successfully loaded into memory"""
        loader = loader.Loader()
