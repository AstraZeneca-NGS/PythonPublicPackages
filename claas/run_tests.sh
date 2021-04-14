#!/bin/bash -l
# This script will install and activate test_env environment, and all requirements.
set -e
set -o pipefail

basedir=$(dirname "$0")

virtualenv -p python3 "${basedir}/test_venv"
source "${basedir}/test_venv/bin/activate"
pip install --upgrade -r "${basedir}/requirements.txt"

pytest --cov=${basedir}/claas/src ${basedir}/claas/tests/ --cov-config ${basedir}/../.coveragerc
echo "Test passed successfully!"

pylint ${basedir}/claas/src --rcfile ${basedir}/../.pylintrc
echo "Pylint passed successfully!"
