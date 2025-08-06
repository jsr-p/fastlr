#!/usr/bin/env bash

venv=${1:-$CONDA_PREFIX}
ini_file=${2:-$(python -c "import os; print(os.path.realpath('native.ini'))")}

echo "Using conda prefix: $venv"
echo "Using native.ini file: $ini_file"

pip install -v \
	-C setup-args="--vsenv" \
	-C setup-args="--native-file=${ini_file}" \
	-C setup-args="-Dconda_prefix=${venv}" \
	-C build-dir=build \
	.
