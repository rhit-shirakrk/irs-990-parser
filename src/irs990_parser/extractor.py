"""
Download and extract information from IRS files
"""

import io
import os
import pathlib

import requests
import zipfile_deflate64 as zipfile

from irs990_parser import custom_exceptions


class IRSZipFileExtractor:
    """
    Extract zip files from a URL request
    """

    TIMEOUT_SEC = 5
    ZIP_EXTENSION_LENGTH = 3

    def __init__(self) -> None:
        pass

    def extract_zip(self, url: str, directory: pathlib.Path) -> pathlib.Path:
        """Extract XML files into a directory

        :param url: The link to the zipped XML files
        :ptype url: str
        :param directory: The directory to extract the zipped XML files
        :ptype directory: pathlib.Path
        :return: The directory containing the XML files
        :rtype: pathlib.Path
        """
        res = requests.get(url, timeout=IRSZipFileExtractor.TIMEOUT_SEC)
        try:
            monthly_reports_directory = pathlib.Path(
                os.path.join(directory, self._get_monthly_reports_folder_name(url))
            )
            with zipfile.ZipFile(io.BytesIO(res.content)) as zip_file:
                zip_file.extractall(path=monthly_reports_directory)

            return monthly_reports_directory
        except zipfile.BadZipFile:
            raise custom_exceptions.InvalidZipFileException(
                f"URL {url} does not yield a ZIP file"
            )

    def _get_monthly_reports_folder_name(self, url: str) -> str:
        # remove the ".zip" from the zip file link
        return url.split("/")[-1][: -(IRSZipFileExtractor.ZIP_EXTENSION_LENGTH + 1)]
