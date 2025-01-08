"""
Custom exceptions for parser
"""


class InvalidZipFileException(Exception):
    """Thrown when a non-zip file is unexpectedly detected"""


class MissingEINException(Exception):
    """Thrown when an IRS form does not contain an EIN field"""
