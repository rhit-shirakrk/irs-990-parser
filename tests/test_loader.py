"""
Tests loader functionality
"""

import pathlib

import pytest

from irs990_parser import loader


class TestLoaderFileValidation:
    """Tests file/section validation checks and connection problems"""

    def test_invalid_file_path_expected_file_not_found_error(self) -> None:
        """Tests if file path does not lead to an existing file"""
        invalid_path = pathlib.Path("non-existent-file.txt")
        with pytest.raises(FileNotFoundError) as excinfo:
            data_loader = loader.Loader(invalid_path)
        assert f"{invalid_path} does not lead to a file" in str(excinfo)

    def test_invalid_file_format_expected_invalid_db_config_format_error(
        self, tmp_path: pathlib.Path
    ) -> None:
        """Tests if config file is not an ini file"""
        fake_dir = tmp_path / "temp"
        fake_dir.mkdir()
        fake_file = fake_dir / "temp.txt"
        fake_file.touch()

        with pytest.raises(ValueError) as excinfo:
            data_loader = loader.Loader(fake_file)
        assert f"{fake_file} does not lead to an ini file" in str(excinfo)
