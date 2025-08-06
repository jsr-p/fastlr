#!/usr/bin/env bash

sudo --preserve-env=CIBW_BEFORE_ALL \
	CIBW_BEFORE_ALL="yum install -y epel-release && yum install -y armadillo-devel" \
	CIBW_BUILD=cp312-manylinux_x86_64 \
	uvx cibuildwheel --output-dir dist
