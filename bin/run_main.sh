#!/bin/bash -x

SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
ENTRYPOINT="${SCRIPT_DIR}/../belong_code_assessment/main.py"
CONFIG_FILE="${SCRIPT_DIR}/../config.yml"
export PYTHONPATH=$PYTHONPATH:"${ENTRYPOINT}/../belong_code_assessment"
python $ENTRYPOINT -c "${CONFIG_FILE}"