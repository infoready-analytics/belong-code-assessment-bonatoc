#!/bin/bash

# setup paths
SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
PYTEST_FILE="${SCRIPT_DIR}/../conftest.py"
CONFIG_FILE="${SCRIPT_DIR}/../config.yml"

# extract URLs from config_file
pedestrian_api_url=$(grep 'pedestrian_api_url:' $CONFIG_FILE | cut -d ' ' -f2 | sed -e 's/^"//' -e 's/"$//')
pedestrian_csv_url=$(grep 'pedestrian_csv_url:' $CONFIG_FILE | cut -d ' ' -f2 | sed -e 's/^"//' -e 's/"$//')

export PYTHONPATH=$PYTHONPATH:"${SCRIPT_DIR}/../belong_code_assessment"
pytest -q $PYTEST_FILE --api_url ${pedestrian_api_url} --csv_url ${pedestrian_csv_url} "${SCRIPT_DIR}/../tests"