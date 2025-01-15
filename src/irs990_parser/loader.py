"""
Stores functionality to load data for transfer into a database
"""

import pandas as pd

from irs990_parser import irs_field_extractor


class Loader:
    """
    Load calculations/field extracted data for a database
    """

    def __init__(self) -> None:
        pass

    def load(
        self, organization_data: irs_field_extractor.OrganizationDataModel
    ) -> None:
        """Load organization data to be saved into a database

        :param organization_data: Extracted data from IRS 990 file
        :type organization_data: irs_field_extractor.OrganizationDataModel
        """

    def get_loaded_records(self) -> int:
        """Return the total number of records

        :return: Number of records
        :rtype: int
        """
        return 1
