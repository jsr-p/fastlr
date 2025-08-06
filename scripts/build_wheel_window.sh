#!/usr/bin/env bash

venv=${1:-$CONDA_PREFIX}
ini_file=${2:-$(python -c "import os; print(os.path.realpath('native.ini'))")}

echo "Using conda prefix: $venv"
echo "Using native.ini file: $ini_file"

export CIBW_CONFIG_SETTINGS_WINDOWS="\
setup-args=--vsenv \
setup-args=--native-file=${ini_file} \
setup-args=-Dconda_prefix=${venv}"

echo "Environment:"
env | grep CIBW

cibuildwheel --output-dir wheelhouse --platform windows
