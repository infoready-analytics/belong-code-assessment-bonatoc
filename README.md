# Belong Code Assessment
This repository contains my response to the Data Engineer coding assessment provided by Belong.

# Overview
The **main.py** script downloads the datasets in the [datasets](#datasets) section below and extracts stats for the:
* Top 10 (most pedestrians) locations by day.
* Top 10 (most pedestrians) locations by month.

These outputs are saved to disk, but can also optionally be uploaded to an S3 bucket as CSV files as per the specifications.

# Project Structure
* belong_code_assessment/: Python package
    * api.py: utils for downloading data over HTTP or JSON via GET requests to the Socrata Open Data API
    * aws.py: uploading files to S3
    * config.py: configuration management
    * logger.py: logging management
    * main.py: CLI entrypoint
    * stats.py: logic for extraction of stats
    * utils.py: general utilities shared across other files
* bin/: bash scripts
    * run_tests.sh: wrapper for running tests
* tests/: Python tests and test data
* config.yml: example configuration
* conftest.py: share fixtures across multiple files
* README.md: this file
* requirements.txt: Python package requirements
* setup.py: package installation script

# Approach
## Design Decisions
### Datasets
The assessment provided two datasets:
* [City of Melbourne Pedestrian Counting - Monthly (counts per hour)](https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-2009-to-Present-counts-/b2ak-trbp)
* [City of Melbourne Pedestrian Counting - Sensor Locations](https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-Sensor-Locations/h57g-5234)

The first task was to perform a data exploration - this was simply downloading the CSV files and using the Python library [Pandas](https://pandas.pydata.org/) to visualise the DataFrames. During this exploration I found that the Sensor Location information was not required for this task, so no code in this repository makes reference to it.

### Data extraction
The data can be extracted either via CSV or using the Socrata Open Data API (SODA). I implemented both solutions, but found the API to be significantly slower without concurrency. I have applied concurrency to speed up the requests, but based on testing the number of workers needs to be at least 6 for it to be faster than downloading the CSV file over HTTP. The code is flexible and will prioritise downloading from the CSV file.

### Python libraries
I have selected the following 3rd party Python libraries:
* [black](https://pypi.org/project/black/): PEP8 compliant code formatter - only custom argument is application of a line length of 100.
* [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html): AWS SDK for Python
* [isort](https://isort.readthedocs.io/en/latest/): PEP8 compliant import sorting - only custom argument is application of a line length of 100.
* [pandas](https://pandas.pydata.org/): used for the majority of the data processing as DataFrames simplify this task immensely
* [pyarrow](https://pypi.org/project/pyarrow/): usage of parquet features in pandas.
* [pytest](https://docs.pytest.org/en/6.2.x/getting-started.html): unit testing
* [PyYAML](https://pypi.org/project/PyYAML/): configuration management

### Testing
As mentioned in [Project Structure](#Project-Structure), tests are defined in the directory **tests**. I have used the **pytest** library for unit tests. The following modules are tested:
* api.py: test downloading CSV data over HTTP and JSON data via SODA.
* aws.py: test reading from and uploading to S3 bucket. 
* config.py: test configuration file can be parsed and loaded.
* stats.py: test stats are calculated as expected.

The logger.py, utils.py and main.py modules do not require testing.

# Running the script
This repository has been tested on a MacBook Pro (16-inch, 2019) and EC2 t2.medium instance.
## Locally
1. Clone the repository
... TODO

2. Create a virtual environment and install dependencies
```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```

3. Run the installer
```bash
cd belong_code_assessment
./bin/install.sh
source venv/bin/activate
```

4. Run the run_main.sh script
```bash
source venv/bin/activate
./bin/run_main.sh
```

## EC2

# Development
