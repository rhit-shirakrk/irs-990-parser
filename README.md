
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

As an example, `python3 main.py --start-year 2019 --end-year 2024` will parse
all XML files from 2019 (inclusive) to 2024 (inclusive).

Any errors will be logged to the `src/errors.log` file. Any bad files will be
stored in the `src/bad_files` directory for easier debugging.
