#!/usr/bin/env bash

source ./env/bin/activate
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=${PYTHONPATH}:${DIR}
nosetests . --config=nose.cfg

radon cc -i "env,tests" --order=SCORE -s --xml . > complexity.xml

flake8 . --output-file flake8.txt

flake8_junit flake8.txt flake8_junit.xml

rm flake8.txt