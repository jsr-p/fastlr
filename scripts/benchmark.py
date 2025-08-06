import itertools as it
import time

import numpy as np
import polars as pl
from numpy.typing import NDArray
import statsmodels.api as sm
from scipy.optimize import minimize
import glum

from fastlr.logreg import generate_data, grad, hess, neg_loglik, IRLSResult
from fastlr import fastlr
from fastlr.utils import run_benchmark_pairs
import typer


app = typer.Typer()


def logit_sm(
    X: NDArray[np.float64],
    y: NDArray[np.float64],
):
    model = sm.Logit(y, X).fit(disp=False)
    return IRLSResult(
        model.params,
        model.mle_retvals.get("iterations", None),
        model.mle_retvals.get("time", 0.0),
    )


def estimate_scipy(
    X: NDArray[np.float64],
    y: NDArray[np.float64],
):
    # scipy.optimize.minimize (Newton-CG)
    return minimize(
        lambda b: neg_loglik(X, y, b),
        x0=np.zeros(X.shape[1]),
        jac=lambda b: grad(X, y, b),
        hess=lambda b: hess(X, b),
        method="Newton-CG",
    )


def bench(X: np.ndarray, y: np.ndarray):
    results = []

    # IRLS
    irls_result = fastlr(X, y, method="python")
    results.append(
        {
            "Method": "IRLS",
            "Time (s)": irls_result.time,
            "Iterations": irls_result.iterations,
        }
    )

    # IRLS cpp
    irls_result_cpp = fastlr(X, y, method="cpp")
    results.append(
        {
            "Method": "IRLS cpp",
            "Time (s)": irls_result_cpp.time,
            "Iterations": irls_result_cpp.iterations,
        }
    )

    start = time.perf_counter()
    res = estimate_scipy(X, y)
    minimize_time = time.perf_counter() - start
    results.append(
        {
            "Method": "scipy.minimize",
            "Time (s)": minimize_time,
            "Iterations": res.nit,
        }
    )

    # statsmodels Logit
    start = time.perf_counter()
    model = sm.Logit(y, X).fit(disp=False)
    sm_time = time.perf_counter() - start
    results.append(
        {
            "Method": "statsmodels",
            "Time (s)": sm_time,
            "Iterations": model.mle_retvals.get("iterations", None),
        }
    )
    return results


def proc_results(results: list[dict]) -> pl.DataFrame:
    return pl.DataFrame(results)


def get_lambdas(
    X: np.ndarray,
    y: np.ndarray,
    select: list[str] | None = None,
):
    pairs = {
        "IRLS": lambda: fastlr(X, y, method="python"),
        "IRLS cpp": lambda: fastlr(X, y, method="cpp"),
        "scipy.minimize": lambda: estimate_scipy(X, y),
        "statsmodels": lambda: sm.Logit(y, X).fit(disp=0),
        "glum": lambda: glum.GeneralizedLinearRegressor(
            family="binomial",
            alpha=0,
            fit_intercept=False,
        ).fit(X=X, y=y),
    }
    if select:
        return {k: v for k, v in pairs.items() if k in select}
    return pairs


def benchmark_avg_fixed(
    X: np.ndarray,
    y: np.ndarray,
    repeats: int = 10,
) -> pl.DataFrame:
    print(f"Running benchmarks for {X.shape=} arrays...")
    pairs = get_lambdas(X, y)
    return pl.DataFrame(run_benchmark_pairs(pairs, repeats=repeats))


def benchmark_avg(
    N: int = 10000,
    k: int = 25,
    repeats: int = 10,
    save: bool = True,
    select: list[str] | None = None,
    seed: int = 42,
) -> pl.DataFrame:
    print(f"Running benchmarks for {N=}, {k=}...")
    X, y = generate_data(N, seed=seed)
    #  armadillo assume column-major order
    X, y = np.asfortranarray(X), np.asfortranarray(y)
    pairs = get_lambdas(X, y, select)
    if save:
        pl.DataFrame(X).write_csv(f"data/X_{N}_{k}.csv")
        pl.DataFrame(y).write_csv(f"data/y_{N}_{k}.csv")
    return pl.DataFrame(run_benchmark_pairs(pairs, repeats=repeats))


def agg_cols():
    return [
        pl.col("time").min().round(4).alias("min"),
        pl.col("time").mean().round(4).alias("mean"),
        pl.col("time").median().round(4).alias("median"),
        pl.col("time").max().round(4).alias("max"),
        pl.col("time").std().round(4).alias("std"),
    ]


@app.command()
def bench_py():
    repeats = 50
    seed = 0
    pairs = it.product([1000, 5000, 10_000, 50_000], [5, 25, 50, 100])
    bench = pl.concat(
        [
            benchmark_avg(N=N, k=k, repeats=repeats, save=True, seed=seed).with_columns(
                N=N, k=k
            )
            for N, k in pairs
        ],
        how="vertical",
    )
    bench.write_csv("output/b_py.csv")

    benchmark_avg_df = (
        bench.group_by("name", "N", "k")
        .agg(agg_cols())
        .with_columns(
            rel_time=pl.col("mean").truediv(pl.col("mean").min().over("N")).round(2),
            Method=pl.col("name"),
        )
        .sort("N", "median")
    )
    with pl.Config(tbl_rows=100):
        print(benchmark_avg_df)


@app.command()
def bench_single(
    method: str,
    # to allow for capitalized flags
    N: int = typer.Option(10_000, "--N", help="Number of observations"),
    k: int = 25,
    repeats: int = 10,
):
    print(f"Running benchmark for {method} with {N=}, {k=}, {repeats=}")
    print(benchmark_avg(N, k, repeats, save=False, select=[method]).select(agg_cols()))


@app.command()
def misc(): ...


if __name__ == "__main__":
    app()
