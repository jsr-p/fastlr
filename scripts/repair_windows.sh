#!/usr/bin/env bash

# Repair a wheel for Windows by adding OpenBLAS DLLs
# The openblas.dll is assumed to be inside the conda environment's Library/bin
# directory.

set -xe

WHEEL="$1"
DEST_DIR="$2"

conda_path=${CONDA_PREFIX}/Library/bin/

# add openblas.dll to the wheel and repkg
delvewheel repair --add-path "$conda_path" -w "$DEST_DIR" "$WHEEL"
