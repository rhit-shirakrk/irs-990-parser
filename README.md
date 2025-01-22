
# Installation

First, ensure you have Python 3.10 installed. The reason is an external
dependency to extract zip files ([`zipfile-deflate64`](https://github.com/brianhelba/zipfile-deflate64)) provides support
only up to Python 3.10.

Next, install dependencies via `pip install -r requirements.txt`

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

# Data Sources

## First Name Gender Probabilities

- [World Gender Name Dictionary, Harvard Dataverse (WGND 2.0)](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/MSEGSJ)

## Nonprofit Organization Data

- IRS 990 Forms [downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)
- Candid Demographic Self-Reporting [download](https://info.candid.org/candid-demographics)
