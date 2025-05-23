"""
Unit tests for retriving links to index and zip files
"""

import pytest
from pytest_unordered import unordered

from irs990_parser import link_retriever


class TestIRS990LinkRetriever:
    """
    Unit tests for IRS990LinkRetriever class
    """

    INDEX_LINKS = [
        "https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv",
        "https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv",
        "https://apps.irs.gov/pub/epostcard/990/xml/2022/index_2022.csv",
        "https://apps.irs.gov/pub/epostcard/990/xml/2021/index_2021.csv",
        "https://apps.irs.gov/pub/epostcard/990/xml/2020/index_2020.csv",
        "https://apps.irs.gov/pub/epostcard/990/xml/2019/index_2019.csv",
    ]

    YEAR_TO_ZIP_LINKS = {
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
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11A.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11B.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_11C.zip",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/2024_TEOS_XML_12A.zip",
        ],
    }

    def test_earlier_than_earliest_start_year_expected_value_error(self) -> None:
        """
        Tests for a start year earlier than 2019
        """
        invalid_start_year = link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR - 1
        current_year = 2024
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(invalid_start_year, current_year)
        assert (
            f"Invalid start year {invalid_start_year}. The earliest available year is {link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR}"
            in str(excinfo.value)
        )

    def test_later_than_current_year_start_year_expected_value_error(self) -> None:
        """
        Tests for a start year later than the most recent year with IRS files published
        """
        current_year = 2024
        invalid_start_year = current_year + 1
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(invalid_start_year, current_year)
        assert (
            f"Invalid start year {invalid_start_year}. The latest available year is {current_year}"
            in str(excinfo.value)
        )

    def test_later_than_current_year_end_year_expected_value_error(self) -> None:
        """
        Tests for an end year later than the current year
        """
        current_year = 2024
        invalid_end_year = current_year + 1
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(current_year, invalid_end_year)
        assert (
            f"Invalid end year {invalid_end_year}. The latest available year is {current_year}"
            in str(excinfo.value)
        )

    def test_end_year_earlier_than_start_year_expected_value_error(self) -> None:
        """
        Tests for an end year earlier than the start year
        """
        current_year = 2024
        invalid_end_year = current_year - 1
        with pytest.raises(ValueError) as excinfo:
            link_retriever.IRS990LinkRetriever(current_year, invalid_end_year)
        assert (
            f"Invalid end year {invalid_end_year}. The earliest available year is {current_year}"
            in str(excinfo.value)
        )

    def test_get_index_csv_links_zero_year_range_expected_valid(self) -> None:
        """
        Tests for proper fetching of links to index files for a single year
        """
        reverse_index = 1
        for start_year in range(
            link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR, 2024
        ):
            expected_link = TestIRS990LinkRetriever.INDEX_LINKS[-reverse_index]
            irs_link_retriever = link_retriever.IRS990LinkRetriever(
                start_year, start_year
            )
            assert [expected_link] == irs_link_retriever.get_index_csv_links()
            reverse_index += 1

    def test_get_index_csv_links_one_year_range_expected_valid(self) -> None:
        """
        Tests for proper fetching of links to index files across two years
        """
        expected_links = TestIRS990LinkRetriever.INDEX_LINKS[-3:-1]
        assert (
            expected_links
            == link_retriever.IRS990LinkRetriever(
                link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR + 1,
                link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR + 2,
            ).get_index_csv_links()
        )

    def test_get_index_csv_links_max_year_range_expected_valid(self) -> None:
        """
        Tests for proper fetching of links to index files for a single year
        """
        current_year = 2024
        irs_link_retriever = link_retriever.IRS990LinkRetriever(
            link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR, current_year
        )
        assert (
            TestIRS990LinkRetriever.INDEX_LINKS
            == irs_link_retriever.get_index_csv_links()
        )

    def test_get_zip_links_expected_valid(self) -> None:
        """
        Tests for proper fetching of links to zip files. 2024 will
        be omitted since more files will be uploaded later.
        """
        for year in range(link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR, 2024):
            assert (
                TestIRS990LinkRetriever.YEAR_TO_ZIP_LINKS[year]
                == link_retriever.IRS990LinkRetriever(year, year).get_zip_links()
            )

    def test_get_zip_links_one_year_range_expected_valid(self) -> None:
        """
        Tests for proper fetching of links to zip files in a 1 year
        range
        """
        start_year = 2019
        end_year = 2020
        expected_links = (
            TestIRS990LinkRetriever.YEAR_TO_ZIP_LINKS[start_year]
            + TestIRS990LinkRetriever.YEAR_TO_ZIP_LINKS[end_year]
        )
        assert (
            unordered(expected_links)
            == link_retriever.IRS990LinkRetriever(start_year, end_year).get_zip_links()
        )

    def test_get_zip_links_max_year_range_expected_valid(self) -> None:
        """
        Tests for proper fetching of all links to zip files
        """
        expected_links = []
        for links in TestIRS990LinkRetriever.YEAR_TO_ZIP_LINKS.values():
            expected_links.extend(links)

        assert (
            unordered(expected_links)
            == link_retriever.IRS990LinkRetriever(
                link_retriever.IRS990LinkRetriever.EARLIEST_START_YEAR,
                link_retriever.IRS990LinkRetriever.LATEST_END_YEAR,
            ).get_zip_links()
        )
