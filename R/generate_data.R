#' Generate synthetic logistic regression data
#' Function taken from fastglm package
#'
#' @param N Number of observations
#' @param k Number of predictors
#' @param seed seed for random number generation
#' @return A list with matrix `X` and vector `y`
#' @export
generate_data <- function(N, k = 25, seed = 0) {
  set.seed(seed)

  n.vars <- k
  indices <- seq_len(n.vars)
  Sigma <- 0.99^abs(outer(indices, indices, FUN = "-"))
  mu <- runif(n.vars, min = -1, max = 1)
  X <- MASS::mvrnorm(n = N, mu = mu, Sigma = Sigma)
  coefficientss <- runif(k, min = -0.1, max = 0.1)
  linpred <- X[, seq_len(k), drop = FALSE] %*% coefficientss
  y <- as.integer(drop(linpred) > rnorm(N))

  return(list(X = X, y = y))
}
