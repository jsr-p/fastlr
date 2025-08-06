import fastlr
import typer
from line_profiler import LineProfiler
from fastlr.logreg import irls, generate_data

app = typer.Typer()


def run(
    N: int = 10_000,
    k: int = 25,
    repeats: int = 10,
):
    X, y = generate_data(N, k, seed=42)
    for _ in range(repeats):
        _ = fastlr.fastlr(X, y, method="python")


@app.command()
def prof(
    N: int = typer.Option(10_000, "--N", help="Number of observations"),
    k: int = 25,
):
    lp = LineProfiler()
    lp.add_function(fastlr.fastlr)
    lp.add_function(irls)
    lp.enable_by_count()
    run(N, k)
    lp.print_stats()


if __name__ == "__main__":
    app()
