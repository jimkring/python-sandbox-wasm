#! /bin/bash
echo "compiling requirements"
pip-compile --quiet --resolver=backtracking --output-file requirements.txt requirements.in
echo "compiling requirements-dev"
pip-compile --quiet --resolver=backtracking --output-file requirements-dev.txt requirements-dev.in
echo "requirements compiled"
