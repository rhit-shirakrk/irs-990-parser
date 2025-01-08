"""
Custom exceptions for parser
"""


class InvalidZipFileException(Exception):
    """Thrown when a non-zip file is unexpectedly detected"""


class MissingFilerException(Exception):
    """Thrown when an IRS form does not contain a Filer section"""


class MissingEINException(Exception):
    """Thrown when an IRS form does not contain an EIN field"""


class MissingOrganizationNameException(Exception):
    """Thrown when an IRS form does not contain an organization name"""
