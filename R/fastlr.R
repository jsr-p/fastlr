#' Fast Logistic Regression Estimator (IRLS)
#'
#' Estimate logistic regression coefficients using iteratively reweighted least squares.
#'
#' @param X A numeric matrix of predictors (design matrix).
#' @param y A numeric vector of binary outcomes (0/1).
#' @param tol A numeric tolerance for convergence (default is 1e-8).
#' @param max_iter An integer for the maximum number of iterations (default is 1000).
#'
#' @return A list containing:
#' \describe{
#'   \item{coefficients}{Estimated coefficients (numeric vector).}
#'   \item{iterations}{Number of iterations performed (integer).}
#'   \item{time}{Total runtime in seconds (numeric).}
#'   \item{converged}{Logical indicating convergence.}
#' }
#'
#' @examples
#' X <- matrix(rnorm(100 * 3), 100, 3)
#' y <- rbinom(100, 1, 0.5)
#' res <- fastlr(X, y)
#'
#' @export
fastlr <- function(X, y, tol = 1e-8, max_iter = 1000L) {
  .Call(`_fastlr_estimate_irls`, X, y, tol, max_iter)
}
