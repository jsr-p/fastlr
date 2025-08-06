#!/usr/bin/env bash

# testing the armadillo implementation inside cpp only
g++ -std=c++17 -O2 -o scripts/cpp_test \
	scripts/cpp_test.cpp \
	src/core/irls.cpp \
	-larmadillo \
	-Isrc/core

# -ggdb for prof annotate; however couldn't get it to work
g++ -std=c++17 -ggdb -O0 \
	-fno-omit-frame-pointer \
	-o scripts/cpp_test_db \
	scripts/cpp_test.cpp \
	src/core/irls.cpp \
	-larmadillo \
	-Isrc/core


if ! grep -q "cpp_test" .gitignore ; then
	echo "cpp_test" >> .gitignore
	echo "cpp_test_db" >> .gitignore
	echo "cpp_test_dbgprof " >> .gitignore
fi
