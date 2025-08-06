#!/usr/bin/env bash
set -e

# Check for required tools
for cmd in pybind11-stubgen ruff; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: $cmd is not in PATH" >&2
    exit 1
  fi
done

# Generate stubs
pybind11-stubgen fastlr._fastlr

# Format with ruff
ruff format stubs/fastlr/_fastlr.pyi

mv stubs/fastlr/_fastlr.pyi src/fastlr/_fastlr.pyi
