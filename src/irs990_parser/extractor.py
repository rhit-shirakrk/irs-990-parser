"""
Download and extract information from IRS files
"""

import io
import os
import pathlib

import requests
import zipfile_deflate64 as zipfile

from irs990_parser import custom_exceptions


class IRSExtractor:
    TIMEOUT_SEC = 5
    ZIP_EXTENSION_LENGTH = 3

    def __init__(self) -> None:
        pass

    def extract_zip(self, url: str, directory: pathlib.Path) -> None:
        """Extract XML files into a directory

        :param url: The link to the zipped XML files
        :ptype url: str
        :param directory: The directory to extract the zipped XML files
        :ptype directory: pathlib.Path
        """
        res = requests.get(url, timeout=IRSExtractor.TIMEOUT_SEC)
        try:
            with zipfile.ZipFile(io.BytesIO(res.content)) as zip_file:
                zip_file.extractall(
                    path=os.path.join(
                        directory, self._get_monthly_reports_folder_name(url)
                    )
                )
        except zipfile.BadZipFile:
            raise custom_exceptions.InvalidZipFileException(
                f"URL {url} does not yield a ZIP file"
            )

    def _get_monthly_reports_folder_name(self, url: str) -> str:
        # remove the ".zip" from the zip file link
        return url.split("/")[-1][: -(IRSExtractor.ZIP_EXTENSION_LENGTH + 1)]
