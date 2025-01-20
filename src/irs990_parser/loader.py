"""
Stores functionality to load data for transfer into a database
"""

import configparser
import os
import pathlib

import pandas as pd
import sqlalchemy

from irs990_parser import irs_field_extractor


class Loader:
    """Load a database config file to upload data to a database

    :param ini_config_path: The path to the ini config file
    :type ini_config_path: pathlib.Path
    """

    CONFIG_FILE_EXTENSION = ".ini"
    CONFIG_SECTION = "irs_db"
    USER_CONFIG_KEY = "user"
    PASSWORD_CONFIG_KEY = "password"
    HOSTNAME_CONFIG_KEY = "hostname"
    PORT = 3306
    DATABASE_CONFIG_KEY = "database"
    TABLE_NAME = "Organizations"

    def __init__(self, ini_config_path: pathlib.Path) -> None:
        self._validate_config_file(ini_config_path)
        config = configparser.ConfigParser()
        config.read(ini_config_path)
        self.user = config.get(Loader.CONFIG_SECTION, Loader.USER_CONFIG_KEY)
        self.hostname = config.get(Loader.CONFIG_SECTION, Loader.HOSTNAME_CONFIG_KEY)
        self.password = config.get(Loader.CONFIG_SECTION, Loader.PASSWORD_CONFIG_KEY)
        self.database = config.get(Loader.CONFIG_SECTION, Loader.DATABASE_CONFIG_KEY)

    def _validate_config_file(self, ini_config_path: pathlib.Path) -> None:
        """Ensure config file exists and is an ini file

        :param ini_config_path: The path to the config file
        :type ini_config_path: pathlib.Path
        :raises FileNotFoundError: The path does not lead to an existing file
        :raises ValueError: The path does not lead to an ini file
        :raises ValueError: The file is missing the specified config section
        """
        if not os.path.exists(ini_config_path):
            raise FileNotFoundError(f"{ini_config_path} does not lead to a file")

        _, file_extension = os.path.splitext(ini_config_path)
        if file_extension != Loader.CONFIG_FILE_EXTENSION:
            raise ValueError(f"{ini_config_path} does not lead to an ini file")

    def load_into_db(
        self, organizations: list[irs_field_extractor.OrganizationDataModel]
    ) -> None:
        """Load saved records into a database

        :param organizations: Data representations of organizations
        :type organizations: list[irs_field_extractor.OrganizationDataModel]
        """
        connection = self._get_db_connection()
        records_df = pd.DataFrame([record.__dict__ for record in organizations])
        records_df.drop_duplicates(subset="ein", keep="first", inplace=True)
        records_df.to_sql(
            Loader.TABLE_NAME, connection, index=False, if_exists="append"
        )
        connection.dispose()

    def _get_db_connection(self) -> sqlalchemy.Engine:
        """Creates connection to database

        :return: Connection to database
        :rtype: sqlalchemy.Engine
        """
        return sqlalchemy.create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.hostname}:{Loader.PORT}/{self.database}"
        )
