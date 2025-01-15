"""
Stores functionality to load data for transfer into a database
"""

import pandas as pd

from irs990_parser import irs_field_extractor


class Loader:
    """
    Load calculations/field extracted data for a database
    """

    def __init__(
        self, organizations: list[irs_field_extractor.OrganizationDataModel]
    ) -> None:
        self.records = organizations
