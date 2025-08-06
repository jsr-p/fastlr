#include "irls.hpp"
#include <armadillo>
#include <chrono>

using std::chrono::duration;
using std::chrono::high_resolution_clock;
using std::chrono::milliseconds;

IRLSResult irls(const arma::mat &X, const arma::vec &y, double tol,
                int max_iter) {
    const int p = X.n_cols;
    arma::vec beta = arma::zeros<arma::vec>(p);
    arma::vec beta_next;

    int iters = 0;
    bool changed = true;

    arma::mat Xt = X.t(); // transpose once only

    auto t1 = high_resolution_clock::now();
    while (changed && iters < max_iter) {
        arma::vec eta = X * beta;
        arma::vec mu = 1.0 / (1.0 + arma::exp(-eta)); // expit
        arma::vec W = arma::clamp(mu % (1 - mu), 1e-10, 1.0);
        arma::vec z = eta + (y - mu) / W;
        beta_next = arma::solve(Xt * (X.each_col() % W), Xt * (W % z),
                                arma::solve_opts::fast);
        changed = arma::any(arma::abs(beta_next - beta) > tol);
        beta = beta_next;
        ++iters;
    }
    duration<double, std::milli> time = high_resolution_clock::now() - t1;
    return IRLSResult{beta, iters, time.count() / 1000.0, !changed};
}
