library(microbenchmark)
library(ggplot2)
library(fastglm)
library(fastlr)


x <- as.matrix(read.csv("data/X.csv", header = TRUE))
y <- as.numeric(read.csv("data/y.csv", header = TRUE)[["y"]])

cat("Running benchmark\n")
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

print(ct)

p <- autoplot(ct, log = FALSE) +
  stat_summary(fun.y = median, geom = "point", size = 2) +
  scale_x_discrete(labels = c("fastlr_rcpp" = "fastlr-rcpp"))
ggsave(p, file = "output/fastglm_bm.png")

sink("output/sessioninfo.txt")
cat("Session info:\n")
print(sessionInfo())
sink()
