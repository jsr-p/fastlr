import time

from collections.abc import Callable


def run_benchmark(benchmark: Callable, reps: int = 5) -> list[float]:
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        benchmark()
        end = time.perf_counter()
        times.append(end - start)
    return times


def run_benchmark_pairs(
    pairs: dict[str, Callable],
    repeats: int,
) -> list[dict]:
    res = []
    for name, fn in pairs.items():
        times = run_benchmark(fn, reps=repeats)
        res.extend([{"name": name, "time": t} for t in times])
        print(f"Finished with {name=}")
    return res


__all__ = [
    "run_benchmark",
    "run_benchmark_pairs",
]
