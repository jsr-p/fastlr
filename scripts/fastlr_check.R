library(fastlr)

# Read data
X <- as.matrix(read.csv("data/X.csv", header = TRUE))
y <- as.numeric(read.csv("data/y.csv", header = TRUE)[["y"]])

# Run IRLS
fit <- fastlr(X, y)
write.csv(
  data.frame(coefs = fit$coefficients),
  file = "data/coefs_fastlrR.csv",
  row.names = FALSE
)
