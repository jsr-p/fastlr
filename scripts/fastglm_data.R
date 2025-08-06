set.seed(123)
n.obs <- 10000
n.vars <- 100
x <- matrix(rnorm(n.obs * n.vars, sd = 3), n.obs, n.vars)
Sigma <- 0.99^abs(outer(1:n.vars, 1:n.vars, FUN = "-"))
x <- MASS::mvrnorm(n.obs, mu = runif(n.vars, min = -1), Sigma = Sigma)
y <- 1 * (drop(x[, 1:25] %*% runif(25, min = -0.1, max = 0.10)) > rnorm(n.obs))

write.csv(x, "data/X.csv", row.names = FALSE)
write.csv(data.frame(y = y), "data/y.csv", row.names = FALSE)

N <- 10000
write.csv(x[1:N, 1:5], "data/X_s.csv", row.names = FALSE)
write.csv(data.frame(y = y[1:N]), "data/y_s.csv", row.names = FALSE)
