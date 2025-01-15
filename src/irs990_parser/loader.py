"""
Stores functionality to load data for transfer into a database
"""

import configparser
import pathlib
from typing import Optional

import pandas as pd
import sqlalchemy

from irs990_parser import irs_field_extractor


class Loader:
    """
    Load calculations/field extracted data for a database
    """

    CONFIG_SECTION = "irs_db"
    USER_CONFIG_KEY = "user"
    PASSWORD_CONFIG_KEY = "password"
    HOSTNAME_CONFIG_KEY = "hostname"
    PORT = 3306
    DATABASE_CONFIG_KEY = "database"
    TABLE_NAME = "Organizations"

    def __init__(
        self, organizations: list[irs_field_extractor.OrganizationDataModel]
    ) -> None:
        self.records = organizations

    def load_into_db(self, db_config_path: pathlib.Path) -> None:
        """Load saved records into a database

        :param db_config_path: Path to database credentials file
        :type db_config_path: pathlib.Path
        """
        connection = self._get_db_connection(db_config_path)
        records_df = pd.DataFrame([record.__dict__ for record in self.records])
        records_df.to_sql(
            Loader.TABLE_NAME, connection, index=False, if_exists="append"
        )
        connection.dispose()

    def _get_db_connection(self, db_config_path: pathlib.Path) -> sqlalchemy.Engine:
        """Creates connection to database

        :param db_config_path: Path to database credentials file
        :type db_config_path: pathlib.Path
        :return: Connection to database
        :rtype: sqlalchemy.Engine
        """
        config = configparser.ConfigParser()
        config.read(db_config_path)
        user = config.get(Loader.CONFIG_SECTION, Loader.USER_CONFIG_KEY)
        hostname = config.get(Loader.CONFIG_SECTION, Loader.HOSTNAME_CONFIG_KEY)
        password = config.get(Loader.CONFIG_SECTION, Loader.PASSWORD_CONFIG_KEY)
        database = config.get(Loader.CONFIG_SECTION, Loader.DATABASE_CONFIG_KEY)

        return sqlalchemy.create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{hostname}:{Loader.PORT}/{database}"
        )
