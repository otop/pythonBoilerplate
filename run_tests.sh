#!/usr/bin/env bash

MAX_COMPLEXITY="D"      # can be from "A" to "F" where "A" is the lowest

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/env/bin/activate
export PYTHONPATH=${PYTHONPATH}:${DIR}
nosetests . --config=nose.cfg

radon cc -i "env,tests" --order=SCORE -s --xml . > complexity.xml

radon cc -i "env,tests" --order=ALPHA -s -n=${MAX_COMPLEXITY} . 1>&2

flake8 . --output-file flake8.txt

flake8_junit flake8.txt flake8_junit.xml

echo "\n"
flake8 --statistics --count -qq 1>&2

rm flake8.txt