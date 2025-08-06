library(fastglm)

# Read data
X <- as.matrix(read.csv("data/X.csv", header = TRUE))
y <- as.numeric(read.csv("data/y.csv", header = TRUE)[["y"]])

# estimate a single model and export coefficientsficients for testing
coefs <- fastglm(X, y, family = binomial())$coefficients
write.csv(as.data.frame(coefs), file = "data/coefs.csv", row.names = FALSE)
