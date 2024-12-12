"""
Download IRS 990 files and save at specified directory
"""

import os
import pathlib


class IRS990FileDownloader:
    def __init__(self, directory: pathlib.Path) -> None:
        if os.path.isdir(directory):
            self.directory = directory
        raise NotADirectoryError(f"Invalid directory {directory}")
