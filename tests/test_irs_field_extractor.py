"""
Tests all implementations of IRSFieldExtractor
"""


class TestIRSFieldExtractor:
    """
    Tests for edge cases in IRS fields
    """

    def test_ein_extractor_expected_381357951(self) -> None:
        """Tests for valid EIN extraction"""
        ein_extractor = EINExtractor()
