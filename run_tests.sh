#!/usr/bin/env bash
set -e

MAX_COMPLEXITY="D"      # can be from "A" to "F" where "A" is the lowest
SKIP_DIRS="env,tests"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "Activating env..."
source ${DIR}/env/bin/activate

echo -e "Export environ vars..."
export PYTHONPATH=${PYTHONPATH}:${DIR}

echo -e "Run tests..."
nosetests . --config=nose.cfg

echo -e "Compute CC..."
radon cc -i ${SKIP_DIRS} --order=SCORE -s --xml . > complexity.xml

echo -e "Check CC"
radon cc -i ${SKIP_DIRS} --order=ALPHA -s -n=${MAX_COMPLEXITY} . 1>&2

if [[ $(radon cc -i ${SKIP_DIRS} --order=ALPHA -s -n=${MAX_COMPLEXITY} . ) ]]; then
    exit 1
fi

echo -e "Run flake8..."
flake8 . --output-file flake8.txt || true       # continue execution if failed
echo -e "Create flake8 xml file"
flake8_junit flake8.txt flake8_junit.xml
rm flake8.txt

echo -e "\nCheck flake8..."
flake8 --statistics --count -qq 1>&2
