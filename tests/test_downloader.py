"""
Unit tests for retriving links to index and zip files
"""

from datetime import datetime

import pytest
from pytest_unordered import unordered

from irs990_parser import constants, link_retriever


class TestIRS990LinkRetriever:
    """
    Unit tests for IRS990LinkRetriever class
    """

    YEAR_TO_ZIP_LINKS = {
        2018: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/2018_TEOS_XML_CT1.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/2018_TEOS_XML_CT2.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/2018_TEOS_XML_CT3.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_1.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_2.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_3.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_4.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_5.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_6.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/download990xml_2018_7.zip",
        ],
        2019: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/2019_TEOS_XML_CT1.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_1.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_2.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_3.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_4.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_5.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_6.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_7.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/download990xml_2019_8.zip",
        ],
        2020: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/2020_TEOS_XML_CT1.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_1.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_2.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_3.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_4.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_5.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_6.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_7.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/download990xml_2020_8.zip",
        ],
        2021: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01C.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01D.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01E.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01F.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01G.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/2021_TEOS_XML_01H.zip",
        ],
        2022: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01C.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01D.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01E.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_01F.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_11A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_11B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/2022_TEOS_XML_11C.zip",
        ],
        2023: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_01A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_02A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_03A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_04A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_05A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_05B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_06A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_07A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_08A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_09A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_10A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_11A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_11B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_11C.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/2023_TEOS_XML_12A.zip",
        ],
        2024: [
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_01A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_02A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_03A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_04A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_05A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_05B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_06A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_07A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_08A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_09A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_10A.zip",
        ],
    }

    def test_earlier_than_2018_start_year_expected_value_error(self) -> None:
        """
        Tests for a start year earlier than 2018
        """
        invalid_start_year = constants.EARLIEST_START_YEAR - 1
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(invalid_start_year)
        assert (
            f"Invalid start year {invalid_start_year}. The earliest available year is {constants.EARLIEST_START_YEAR}"
            in str(excinfo.value)
        )

    def test_later_than_current_year_start_year_expected_value_error(self) -> None:
        """
        Tests for a start year later than the current year
        """
        current_year = datetime.now().year
        invalid_start_year = current_year + 1
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(invalid_start_year)
        assert (
            f"Invalid start year {invalid_start_year}. The latest available year is {current_year}"
            in str(excinfo.value)
        )

    def test_later_than_current_year_end_year_expected_value_error(self) -> None:
        """
        Tests for an end year later than the current year
        """
        current_year = datetime.now().year
        invalid_end_year = current_year + 1
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(current_year, invalid_end_year)
        assert (
            f"Invalid end year {invalid_end_year}. The latest available year is {current_year}"
            in str(excinfo.value)
        )

    def test_get_index_csv_links_expected_valid(self) -> None:
        """
        Tests for proper fetching of links to index files
        """
        INDEX_LINKS = [
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/index_2022.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/index_2021.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/index_2020.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/index_2019.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/index_2018.csv",
        ]
        current_year = datetime.now().year
        for year in range(constants.EARLIEST_START_YEAR, current_year):
            irs_link_retriever = link_retriever.IRS990LinkRetriever(year)
            assert INDEX_LINKS == irs_link_retriever.get_index_csv_links()
            INDEX_LINKS.pop()

    def test_get_zip_links_expected_valid(self) -> None:
        """
        Tests for properly fetching of zip links
        """
        for test_year in range(constants.EARLIEST_START_YEAR, datetime.now().year + 1):
            expected_zip_links = [
                zip_link
                for year, zip_links in TestIRS990LinkRetriever.YEAR_TO_ZIP_LINKS.items()
                if year >= test_year
                for zip_link in zip_links
            ]
            irs_link_retriever = link_retriever.IRS990LinkRetriever(test_year)
            assert irs_link_retriever.get_zip_links() == unordered(expected_zip_links)
