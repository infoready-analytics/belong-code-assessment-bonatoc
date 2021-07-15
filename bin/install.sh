#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "$0")"; pwd)
VENV_DIR="${SCRIPT_DIR}/../venv"
REQUIREMENTS_FILE="${SCRIPT_DIR}/../requirements.txt"

# install venv
python3 -m venv $VENV_DIR
source "${VENV_DIR}/bin/activate"

# install dependencies
pip install --upgrade cython setuptools pip wheel
pip install -r "${REQUIREMENTS_FILE}"

pushd .
cd "${SCRIPT_DIR}/../" && pip install .
popd