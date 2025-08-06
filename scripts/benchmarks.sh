#!/usr/bin/env bash

export OPENBLAS_NUM_THREADS=1  # important to avoid multithreading issues

set -e

# GLM data benchmark
Rscript scripts/fastglm_data.R
Rscript scripts/fastglm_bm.R

# Python benchmark
python scripts/benchmark.py bench-py

# R implementations on the same data from Python
Rscript scripts/fastglm_bm_multiple.R

# Plot results and create table
Rscript scripts/plot_res.R
python scripts/table.py
