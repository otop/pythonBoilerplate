#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ${DIR}/env/bin/activate
export PYTHONPATH=${PYTHONPATH}:${DIR}
nosetests . --config=nose.cfg

radon cc -i "env,tests" --order=SCORE -s --xml . > complexity.xml

flake8 . --output-file flake8.txt

flake8_junit flake8.txt flake8_junit.xml

echo "\n"
flake8 --statistics --count -qq

rm flake8.txt