
# Installation

First, ensure you have Python 3.10 installed. The reason is an external
dependency to extract zip files ([`zipfile-deflate64`](https://github.com/brianhelba/zipfile-deflate64)) provides support
only up to Python 3.10.

- This is used because the IRS zip files used a proprietary compression
algorithm, which causes issues with Python's `zipfile` library

Dependencies are documented in the `pyproject.toml` file and the `requirements/`
directory.

- `common.txt` are the dependencies required to run the pipeline
- `dev.txt` are dependencies used specifically during development (i.e., testing)

To install dependencies:

- `pip install -r requirements/common.txt`
- `pip install -r requirements/dev.txt`

# Usage

The `main.py` class must be run with start and end year parameters to indicate
the range of years to parse IRS 990 xml files.

These files are extracted into temporary directories to reduce redundant storage
of information, as the extracted data is intended to be sent to a database.
As each zip link will extract a certain number files, all files will be deleted
after they have been parsed.

As an example, `python3 main.py --start-year 2019 --end-year 2024 --credentials-file creds.ini`
will parse all XML files from 2019 (inclusive) to 2024 (inclusive) and connect
to a database using credentials stored in `creds.ini`.

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
