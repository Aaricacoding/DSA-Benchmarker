"""
benchmarker.py — measures actual runtime of each algorithm
across input sizes and returns structured results.
"""

import time
import random
import tracemalloc
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class BenchmarkResult:
    algorithm: str
    category: str
    input_sizes: list[int]
    times_ms: list[float]
    memory_kb: list[float]
    complexity: str          # e.g. "O(n log n)"
    description: str


def _measure(fn: Callable, data) -> tuple[float, float]:
    """Returns (elapsed_ms, peak_memory_kb)."""
    tracemalloc.start()
    t0 = time.perf_counter()
    fn(data)
    elapsed = (time.perf_counter() - t0) * 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return round(elapsed, 4), round(peak / 1024, 3)


def benchmark(
    algorithms: dict[str, Callable],
    input_sizes: list[int],
    data_factory: Callable[[int], any],
    category: str,
    complexities: dict[str, str],
    descriptions: dict[str, str],
    repeats: int = 3,
) -> list[BenchmarkResult]:
    results = []
    for name, fn in algorithms.items():
        times, mems = [], []
        for n in input_sizes:
            run_times, run_mems = [], []
            for _ in range(repeats):
                data = data_factory(n)
                t, m = _measure(fn, data)
                run_times.append(t)
                run_mems.append(m)
            times.append(round(sum(run_times) / repeats, 4))
            mems.append(round(sum(run_mems) / repeats, 3))
        results.append(BenchmarkResult(
            algorithm=name,
            category=category,
            input_sizes=input_sizes,
            times_ms=times,
            memory_kb=mems,
            complexity=complexities.get(name, "?"),
            description=descriptions.get(name, ""),
        ))
    return results
