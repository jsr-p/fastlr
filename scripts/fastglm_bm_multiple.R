library(microbenchmark)
library(ggplot2)
library(fastglm)
library(fastlr)
library(dplyr)
library(purrr)
library(glue)


bm <- function(N, k) {
  # Read data
  x <- as.matrix(read.csv(paste0("data/X_", N, "_", k, ".csv"), header = TRUE))
  y <- as.numeric(read.csv(paste0("data/y_", N, "_", k, ".csv"), header = TRUE)[[1]])

  print(glue("Running benchmark for N={N} and k={k}"))

  ct <- microbenchmark(
    glm.fit = {
      gl1 <- glm.fit(x, y, family = binomial())
    },
    fastglm.qr.cpiv = {
      gf1 <- fastglm(x, y, family = binomial())
    },
    fastglm.qr = {
      gf2 <- fastglm(x, y, family = binomial(), method = 1)
    },
    fastglm.LLT = {
      gf3 <- fastglm(x, y, family = binomial(), method = 2)
    },
    fastglm.LDLT = {
      gf4 <- fastglm(x, y, family = binomial(), method = 3)
    },
    fastlr_rcpp = {
      gf5 <- fastlr(x, y)
    },
    fastglm.qr.fpiv = {
      gf5 <- fastglm(x, y, family = binomial(), method = 4)
    },
    times = 50L
  )
  df <- data.frame(ct) |>
    mutate(time = time / 1e9) |>
    rename(name = expr) |>
    select(name, time) |>
    mutate(N = N, k = k)
  return(df)
}

pairs <- expand.grid(
  N = c(1000, 5000, 10000, 50000),
  k = c(5, 25, 50, 100)
)

results <- pmap(pairs, function(N, k) {
  bm(N, k)
})
out <- bind_rows(results)
write.csv(out, file = "output/b_r.csv", row.names = FALSE)
