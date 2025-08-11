# fastlr: fast(er) logistic regression


- [Usage](#usage)
  - [Python](#python)
  - [R](#r)
- [Installation](#installation)
  - [Python](#python-1)
  - [R](#r-1)
- [Benchmarks](#benchmarks)
  - [Benchmark against `fastglm`](#benchmark-against-fastglm)
  - [Benchmark against Python
    packages](#benchmark-against-python-packages)
  - [Benchmark results as tables](#benchmark-results-as-tables)
- [Development](#development)

This package aims to estimate a logistic regression model in a fast(er)
way using the iteratively reweighted least squares (IRLS) algorithm.
This is implemented using the C++ library
[armadillo](https://arma.sourceforge.net/faq.html). The package provides
R-bindings through
[Rcpp](https://cran.r-Aproject.org/web/packages/Rcpp/index.html) in the
R package `fastlr` and Python-bindings through
[pybind11](https://pybind11.readthedocs.io/en/stable/index.html) in the
Python package `fastlr`; the Python package also provides a pure Python
implementation of the IRLS algorithm.

## Usage

### Python

``` python
from fastlr import fastlr, generate_data

X, y = generate_data(N=10_000, k=10, seed=0)
print(py_res := fastlr(X, y))
```

    FastLrResult(coefficients=array([-0.19547786,  0.26833757, -0.1303476 , -0.03979692, -0.15035753,
           -0.26321948,  0.33105813, -0.19471808,  0.12025924,  0.11202108]), iterations=4, converged=True, time=0.051200235)

``` python
# Alternatively, use the pure Python implementation
print(py_res_simple := fastlr(X, y, method="python"))
```

    FastLrResult(coefficients=array([-0.19547786,  0.26833757, -0.1303476 , -0.03979692, -0.15035753,
           -0.26321948,  0.33105813, -0.19471808,  0.12025924,  0.11202108]), iterations=4, converged=True, time=0.002805208001518622)

``` python
import numpy as np
np.allclose(py_res.coefficients, py_res_simple.coefficients)
```

    True

### R

``` r
library(fastlr)
library(reticulate)

m <- fastlr(py$X, py$y)  # py from reticulate; reticulate nice
print(m)
```

    $coefficients
     [1] -0.19547786  0.26833757 -0.13034760 -0.03979692 -0.15035753 -0.26321948
     [7]  0.33105813 -0.19471808  0.12025924  0.11202108

    $iterations
    [1] 4

    $time
    [1] 0.00205007

    $converged
    [1] TRUE

Thanks [reticulate](https://rstudio.github.io/reticulate/)!

``` r
py_estimates <- py$py_res$coefficients |> as.numeric() 
r_estimates <- m$coefficients

print(py_estimates)
```

     [1] -0.19547786  0.26833757 -0.13034760 -0.03979692 -0.15035753 -0.26321948
     [7]  0.33105813 -0.19471808  0.12025924  0.11202108

``` r
print(r_estimates)
```

     [1] -0.19547786  0.26833757 -0.13034760 -0.03979692 -0.15035753 -0.26321948
     [7]  0.33105813 -0.19471808  0.12025924  0.11202108

``` r
all.equal(py_estimates, r_estimates, tolerance = 1e-6)
```

    [1] TRUE

## Installation

### Python

``` bash
git clone https://github.com/jsr-p/fastlr
cd fastlr
uv sync
pip install .
```

or from pypi

``` bash
pip install fastlr
```

### R

``` bash
git clone https://github.com/jsr-p/fastlr
cd fastlr
Rscript -e 'devtools::install_local(".")'
```

## Benchmarks

To reproduce the benchmarks install the development versions of both
packages and run:

``` bash
just bench
```

### Benchmark against `fastglm`

This benchmark shows the same results as shown in the [fastglm
package](https://github.com/jaredhuling/fastglm?tab=readme-ov-file#quick-usage-overview)
with the `fastlr` (Rcpp) [implementation](src/fastlr_rcpp.cpp) added to
the figure (run on my laptop).

<img src="output/fastglm_bm.png" width="750" />

See [scripts/fastglm_bm.R](scripts/fastglm_bm.R) and the
[Justfile](./blob/main/Justfile#L19).

For the `sessionInfo()` see [here](output/sessioninfo.txt).

BTW:

``` bash
grep 'Running under' output/sessioninfo.txt
```

    Running under: Arch Linux

### Benchmark against Python packages

A benchmark study of this package’s two implementations

- Python [implementation](./blob/main/src/fastlr/logreg.py#L86) of the
  `IRLS` algorithm
- C++ [implementation](src/core/irls.cpp) of the `IRLS` algorithm with
  Python bindings through
  [pybind11](https://pybind11.readthedocs.io/en/stable/index.html)

against:

- [glum](https://github.com/Quantco/glum)
- [statsmodels
  logit](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.html)
- minimal `newton-cg` minimize implementation from
  [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)

for varying sample size $N$ and number of covariates $k$.

See the `generate_data` function
[here](./blob/main/src/fastlr/logreg.py#L57).

#### Benchmark Python implementations

![](output/bench_res.png)

Interestingly, as seen from the figure, the pure Python implementation
is quite fast and comparable to the C++ version!

#### Benchmark R implementations on same setup as above

![](output/bench_res_R.png)

### Benchmark results as tables

- See [here](output/tables.md) for the benchmark results as a table.

## Development
