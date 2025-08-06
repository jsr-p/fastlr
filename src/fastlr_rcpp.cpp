#include "core/irls.hpp"
#include <RcppArmadillo.h>

// [[Rcpp::depends(RcppArmadillo)]]
// [[Rcpp::export("fastlr")]]
Rcpp::List estimate_irls(SEXP X, SEXP y, double tol = 1e-8,
                         int max_iter = 1000) {
    arma::mat X_ = Rcpp::as<arma::mat>(X);
    arma::vec y_ = Rcpp::as<arma::vec>(y);

    IRLSResult result = irls(X_, y_, tol, max_iter);
    return Rcpp::List::create(
        // to R vector
        Rcpp::Named("coefficients") = Rcpp::NumericVector(
            result.coefficients.begin(), result.coefficients.end()),
        Rcpp::Named("iterations") = result.iterations,
        Rcpp::Named("time") = result.time,
        Rcpp::Named("converged") = result.converged);
}
