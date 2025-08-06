#include <armadillo>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include "../core/irls.hpp"

namespace py = pybind11;

using namespace std;
using namespace arma;
using namespace pybind11::literals;

py::dict estimate_irls(py::array_t<double> X_arr, py::array_t<double> y_arr,
                       double tol = 1e-8, int max_iter = 1000) {
    py::buffer_info X_buf = X_arr.request();
    py::buffer_info y_buf = y_arr.request();

    if (X_buf.ndim != 2 || y_buf.ndim != 1)
        throw std::runtime_error("Invalid input dimensions");

    // Wrap NumPy arrays without copying
    arma::mat X(static_cast<double *>(X_buf.ptr), X_buf.shape[0],
                X_buf.shape[1], false, true);
    arma::vec y(static_cast<double *>(y_buf.ptr), y_buf.shape[0], false, true);

    IRLSResult result = irls(X, y, tol, max_iter);

    return py::dict("coefficients"_a = py::array_t<double>(result.coefficients.n_elem,
                                                   result.coefficients.memptr()),
                    "iterations"_a = result.iterations, "time"_a = result.time,
                    "converged"_a = result.converged);
}

void check_arma() {
    arma::arma_version ver;
    std::cout << "Armadillo version: " << ver.major << "." << ver.minor << "."
              << ver.patch << std::endl;

#ifdef ARMA_USE_LAPACK
    std::cout << "LAPACK enabled\n";
#else
    std::cout << "LAPACK not enabled\n";
#endif

#ifdef ARMA_USE_BLAS
    std::cout << "BLAS enabled\n";
#else
    std::cout << "BLAS not enabled\n";
#endif

#ifdef ARMA_USE_ATLAS
    std::cout << "Using ATLAS\n";
#endif

#ifdef ARMA_USE_MKL
    std::cout << "Using MKL\n";
#endif

#ifdef ARMA_USE_OPENBLAS
    std::cout << "Using OpenBLAS\n";
#endif
}

PYBIND11_MODULE(_fastlr, m) {
    m.def("irls", &estimate_irls,
          "Run Iteratively Reweighted Least Squares (IRLS)");
    m.def("check_arma", &check_arma, "Check armadillo info");
}
