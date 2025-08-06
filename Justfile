all: install-R install-py py-stubs checks bench cpp-simple

install-R:
    rm -f src/*.o src/*.so src/RcppExports.* src/core/*.o
    Rscript -e 'Rcpp::compileAttributes()'
    R CMD INSTALL .

check-cran-R:
    rm -f src/*.o src/*.so
    rm -f src/core/*.o src/core/*.so
    Rscript -e 'devtools::check(pkg = ".")'

build-ignore-R:
    Rscript scripts/ignore.R

build-R:
    Rscript -e 'devtools::build(path = ".", quiet = FALSE)'

install-py:
    uv pip install -v .

check-sdist-py:
    rm -f 'dist/*.tar.gz'
    uv build --sdist && tar tvf dist/*.tar.gz

check-sdist-R:
    just build-R
    tar tv fastlr*.tar.gz

tests:
    pytest
    Rscript -e 'testthat::test_dir("r-tests")'

py-stubs:
    bash scripts/generate-stubs.sh

bench: 
    bash scripts/benchmarks.sh | tee output/benchmarks.txt

checks:
    Rscript scripts/fastglm_data.R
    Rscript scripts/fastglm_check.R
    Rscript scripts/fastlr_check.R
    python scripts/fastglm_check.py

cpp-simple:
    bash scripts/compile_misc.sh
    ./scripts/cpp_test

plots:
    Rscript scripts/plot_res.R
    python scripts/table.py
