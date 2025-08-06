import tabx
import polars as pl

df = pl.read_csv("output/b_py.csv")
df_r = pl.read_csv("output/b_r.csv")


def get_res(df: pl.DataFrame):
    return (
        df.with_columns(pl.col("time").mul(1e3))
        .group_by("N", "k", "name")
        .agg(
            pl.col("time").min().round(4).alias("min"),
            pl.col("time").quantile(0.25).round(4).alias("Q1"),
            pl.col("time").mean().round(4).alias("mean"),
            pl.col("time").median().round(4).alias("median"),
            pl.col("time").quantile(0.75).round(4).alias("Q3"),
            pl.col("time").max().round(4).alias("max"),
            pl.col("time").std().round(4).alias("std"),
        )
        .with_columns(
            pl.col("median").rank("min").over("N", "k").alias("rank"),
            pl.col("median")
            .truediv(pl.col("median").min().over("N", "k"))
            .alias("relative"),
        )
        .with_columns(pl.selectors.float().round(1))
        .sort("N", "k", "name")
        .rename(
            {
                "N": "$N$",
                "k": "$k$",
            }
        )
        .select(
            "$N$",
            "$k$",
            "name",
            "rank",
            "relative",
            "min",
            "Q1",
            "mean",
            "median",
            "Q3",
            "max",
            "std",
        )
        .rename({"relative": "$\\frac{t}{t_{min}}$"})
    )


df_c = (
    pl.concat([df, df_r], how="vertical")
    .with_columns(
        pl.col("name").replace(
            {"fastlr_rcpp": "fastlr-rcpp"},
        ),
    )
    .with_columns(
        pl.col("name").cast(
            pl.Enum(
                [
                    "IRLS",
                    "IRLS cpp",
                    "statsmodels",
                    "glum",
                    "scipy.minimize",
                    "fastlr-rcpp",
                    "fastglm.qr.fpiv",
                    "fastglm.LLT",
                    "fastglm.LDLT",
                    "fastglm.qr.cpiv",
                    "fastglm.qr",
                    "glm.fit",
                ]
            )
        ),
    )
)


def construct_table(mods: list[str], outname: str):
    kvals = [5, 25, 50, 100]
    nvals = [1000, 5000, 10_000, 50_000]
    n_mods = len(mods)
    n_nvals = len(nvals)
    n_kvals = len(kvals)
    gp = get_res(df_c.filter(pl.col("name").is_in(mods)))
    tab = tabx.simple_table(
        gp.filter(pl.col("name").is_in(mods)).rows(),
        column_names=gp.columns,
    )
    tab = tab.insert_rows(
        # insert midrules every n_mods rows
        [tabx.Midrule() for _ in range(1, n_nvals * n_kvals * n_mods + 1, n_mods)],
        [i for i in range(1, n_nvals * n_kvals * n_mods + 1, n_mods)],
    )
    tabx.pdf_to_png(tabx.compile_table(tab.render(), output_dir="output", name=outname))


construct_table(
    mods=[
        "IRLS",
        "IRLS cpp",
        "statsmodels",
        "glum",
        "scipy.minimize",
    ],
    outname="pyres",
)

construct_table(
    mods=[
        "fastlr-rcpp",
        "glm.fit",
        "fastglm.qr.fpiv",
        "fastglm.LLT",
        "fastglm.LDLT",
        "fastglm.qr.cpiv",
        "fastglm.qr",
    ],
    outname="rres",
)
