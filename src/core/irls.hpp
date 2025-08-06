#pragma once

#include <armadillo>

struct IRLSResult {
    arma::vec coefficients;
    int iterations;
    double time;
    bool converged;
};

IRLSResult irls(const arma::mat &X, const arma::vec &y, double tol = 1e-8,
                int max_iter = 100);
