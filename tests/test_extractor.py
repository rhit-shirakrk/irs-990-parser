from irs990_parser import extractor


class TestIRSExtractor:
    def test_downloaded_file_is_not_zip_file_expected_unsupported_file_format_error(
        self,
    ):
        """
        Tests if a downloaded file is a zip file
        """
        irs_extractor = extractor.IRSExtractor()
