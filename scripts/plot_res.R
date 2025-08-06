library(ggplot2)
library(readr)
library(dplyr)

# Read data
df <- read_csv("output/b_py.csv") |> mutate(
  name = case_when(
    name == "IRLS" ~ "fastlr-python",
    name == "IRLS cpp" ~ "fastlr-cpp",
    TRUE ~ name
  )
)
df_r <- read_csv("output/b_r.csv") |>
  mutate(name = if_else(name == "fastlr_rcpp", "fastlr-rcpp", name))

plot_data <- function(df) {
  ggplot(df, aes(x = name, y = time, fill = name)) +
    geom_violin(trim = FALSE, alpha = 0.8, width = 2) +
    geom_boxplot(width = 0.2, outlier.shape = NA, alpha = 0.3) +
    facet_grid(N ~ k, scales = "free_y") +
    scale_y_log10() +
    theme_classic() +
    theme(
      text = element_text(size = 22),
      axis.text.x = element_blank(),
      axis.title.x = element_blank(),
      axis.ticks.x = element_blank(),
      strip.text.x = element_text(face = "bold"), # N labels
      strip.text.y = element_text(face = "bold") # k labels
    ) +
    labs(
      title = "Benchmark results by sample size and covariates",
      subtitle = "Each panel shows results for the pair (N, k)",
      x = "Implementation",
      y = "Runtime (log10 seconds)",
      fill = "Implementation"
    )
}

# Save plot
ggsave("output/bench_res.png", plot = plot_data(df), width = 16, height = 12)

ggsave(
  "output/bench_res_R.png",
  plot = plot_data(df_r),
  width = 12,
  height = 12
)

comb <- rbind(
  df_r |>
    filter(
      name %in% c(
        "fastlr-rcpp",
        "fastglm.qr.cpiv",
        "fastglm.LLT",
        "fastglm.LDLT"
      )
    ),
  df |> filter(
    name %in% c(
      "glum",
      "fastlr-python",
      "fastlr-cpp"
    )
  )
)
ggsave(
  "output/bench_res_combined.png",
  plot = plot_data(comb),
  width = 12,
  height = 12
)
