
# Installation

Dependencies are documented in the `pyproject.toml` file and the `requirements/`
directory.

- `common.txt` are the dependencies required to run the pipeline
- `dev.txt` are dependencies used specifically during development (i.e., testing)

To install dependencies (these should be ran while a virtual environment is up):

- `pip install -r requirements/common.txt`
- `pip install -r requirements/dev.txt`

# Usage

Before running the pipeline, ensure that the database you are importing the data
to contains an empty table who's schema matches `db_tables/org_table.sql`. If
not, run the SQL script mentioned to create such a table.

The `main.py` class must be run with a specified directory containing XML files
to upload.

As an example, `python3 main.py --credentials-file creds.ini --xml-directory xml_files_here`
will parse all xml files in the directory `xml_files_here` and connect to a database
using credentials stored in `creds.ini`.

Any errors will be logged to the `src/errors.log` file. Any bad files will be
stored in the `src/bad_files` directory for easier debugging.

# Credentials File

The expected format for `ini` files containing database credentials is:

```python
[irs_db]
user = "USERNAME_HERE"
password = "PASSWORD_HERE"
hostname = "HOSTNAME_HERE"
port = "PORT_HERE"
database = "DATABASE_NAME_HERE"
table_name = "TABLE_NAME"
```

# IRS XML File Format

Since the IRS 990 files are stored in XML format, fields can be found by
indexing specific XML tags

As an example, finding the Employer Identification Number (EIN) requires searching
for the "Filer" tag. Then, nested in that tag, there's an EIN tag that contains
the EIN.

This nested structure continues through all field extractor classes in the
`src/irs990_parser/irs_field_extractor.py` file.

Though the fields are abbreviated, it is mostly clear as to which tag correlates
to which field in the actual [IRS 990 form](https://www.irs.gov/pub/irs-pdf/f990.pdf).

If a tag in the XML file is missing, then that information was not supplied.
This, among other anomalies, exist within the XML files that the tests in the
`tests/` directory attempt to catch. Look at the test names and implementations
for more information.

Sample files containing anomalies that were found in actual IRS XML files are
also available in the `tests/sample_irs_xml_files/` directory.

# Data Sources

- Gender Probabilities: [World Gender Name Dictionary, Harvard Dataverse (WGND 2.0)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MSEGSJ)
- IRS 990 Forms [downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)
