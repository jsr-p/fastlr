#include <armadillo>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

#include "irls.hpp"

/**
 * @brief Load a CSV file into an Armadillo matrix, skipping the header row.
 *
 * @param filename
 * @return
 */
arma::mat load_csv_skip_header(const std::string &filename) {
    std::ifstream file(filename);
    std::stringstream buffer;

    std::string line;
    // Skip header
    std::getline(file, line);

    // Read the rest into buffer
    buffer << file.rdbuf();

    arma::mat result;
    result.load(buffer, arma::csv_ascii);
    return result;
}

void run_irls_benchmark(const arma::mat &X, const arma::vec &y) {
    std::cout << "running benchmark..." << std::endl;
    for (int i = 0; i < 100; ++i) {
        IRLSResult result = irls(X, y); // or your equivalent function
    }
    std::cout << "finished benchmark" << std::endl;
}

int test2() {
    arma::mat X = arma::randn(10000, 100);
    arma::vec y = arma::randi<arma::vec>(10000, arma::distr_param(0, 1));
    run_irls_benchmark(X, y);
    return 0;
}

int test() {
    arma::mat X = load_csv_skip_header("data/X.csv");
    arma::vec y = load_csv_skip_header("data/y.csv");

    std::cout << "Loaded X: " << X.n_rows << "x" << X.n_cols << std::endl;
    std::cout << "Loaded y: " << y.n_rows << " rows\n";

    run_irls_benchmark(X, y);

    return 0;
}

int test_estimates() {
    // arma::mat X = load_csv_skip_header("data/X.csv");
    // arma::vec y = load_csv_skip_header("data/y.csv");

    arma::mat X = load_csv_skip_header("data/X_s.csv");
    arma::vec y = load_csv_skip_header("data/y_s.csv");

    std::cout << "Loaded X: " << X.n_rows << "x" << X.n_cols << std::endl;
    std::cout << "Loaded y: " << y.n_rows << " rows\n";

    IRLSResult res = irls(X, y);

    std::cout << "Beta: " << res.beta.t() << std::endl;
    std::cout << "Iterations: " << res.iterations << std::endl;
    std::cout << "Time taken: " << res.time << " seconds" << std::endl;

    return 0;
}

int main() {
    // running test with simulated data;
    test();
    // test2();
}
