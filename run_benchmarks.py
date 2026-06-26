"""
run_benchmarks.py — entry point.
Runs all algorithm categories, saves charts to results/ and a summary CSV.

Usage:
    python run_benchmarks.py
"""

import random
import os
import csv
import sys
sys.setrecursionlimit(10000)
from algorithms import (
    bubble_sort, selection_sort, insertion_sort,
    merge_sort, quick_sort, heap_sort, timsort_builtin,
    linear_search, binary_search, jump_search, interpolation_search,
    bfs, dfs, dfs_iterative, _make_adj,
)
from benchmarker import benchmark, BenchmarkResult
from charts import plot_time, plot_memory, plot_combined

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


# ── 1. Sorting ─────────────────────────────────────────────────────────────

SORT_SIZES = [100, 250, 500, 1000, 2000, 4000]

sort_results = benchmark(
    algorithms={
        "Bubble Sort":     lambda a: bubble_sort(a),
        "Selection Sort":  lambda a: selection_sort(a),
        "Insertion Sort":  lambda a: insertion_sort(a),
        "Merge Sort":      lambda a: merge_sort(a),
        "Quick Sort":      lambda a: quick_sort(a),
        "Heap Sort":       lambda a: heap_sort(a),
        "Timsort (built-in)": lambda a: timsort_builtin(a),
    },
    input_sizes=SORT_SIZES,
    data_factory=lambda n: [random.randint(0, n * 10) for _ in range(n)],
    category="Sorting",
    complexities={
        "Bubble Sort": "O(n²)", "Selection Sort": "O(n²)",
        "Insertion Sort": "O(n²)", "Merge Sort": "O(n log n)",
        "Quick Sort": "O(n log n) avg", "Heap Sort": "O(n log n)",
        "Timsort (built-in)": "O(n log n)",
    },
    descriptions={
        "Bubble Sort": "Simple comparison sort; swaps adjacent elements.",
        "Selection Sort": "Finds minimum each pass; minimal swaps.",
        "Insertion Sort": "Builds sorted array one element at a time.",
        "Merge Sort": "Divide-and-conquer; stable; guaranteed O(n log n).",
        "Quick Sort": "Partition around pivot; fast in practice.",
        "Heap Sort": "Uses a binary heap; in-place O(n log n).",
        "Timsort (built-in)": "Python's hybrid merge+insertion sort.",
    },
    repeats=4,
)

plot_time(sort_results, title="Sorting Algorithms — Runtime Comparison",
          out=f"{RESULTS_DIR}/sorting_time.png")
plot_memory(sort_results, title="Sorting Algorithms — Peak Memory Usage",
            out=f"{RESULTS_DIR}/sorting_memory.png")
plot_combined(sort_results, title="Sorting — Time vs Memory",
              out=f"{RESULTS_DIR}/sorting_combined.png")
print("✓ Sorting benchmarks done")


# ── 2. Searching ───────────────────────────────────────────────────────────

SEARCH_SIZES = [500, 1000, 5000, 10000, 50000, 100000]

def search_factory(n: int) -> tuple:
    arr = sorted(random.randint(0, n * 5) for _ in range(n))
    target = arr[random.randint(0, n - 1)]
    return arr, target

search_results = benchmark(
    algorithms={
        "Linear Search":        lambda d: linear_search(d),
        "Binary Search":        lambda d: binary_search(d),
        "Jump Search":          lambda d: jump_search(d),
        "Interpolation Search": lambda d: interpolation_search(d),
    },
    input_sizes=SEARCH_SIZES,
    data_factory=search_factory,
    category="Searching",
    complexities={
        "Linear Search": "O(n)",
        "Binary Search": "O(log n)",
        "Jump Search": "O(sqrt n)",
        "Interpolation Search": "O(log log n) avg",
    },
    descriptions={
        "Linear Search": "Scans every element; works on unsorted data.",
        "Binary Search": "Halves search space each step; sorted array required.",
        "Jump Search": "Jumps by √n blocks then linear scan.",
        "Interpolation Search": "Estimates position; fast on uniform distributions.",
    },
    repeats=5,
)

plot_time(search_results, title="Searching Algorithms — Runtime Comparison",
          out=f"{RESULTS_DIR}/searching_time.png")
plot_combined(search_results, title="Searching — Time vs Memory",
              out=f"{RESULTS_DIR}/searching_combined.png")
print("✓ Searching benchmarks done")


# ── 3. Graph Traversal ─────────────────────────────────────────────────────

GRAPH_SIZES = [100, 300, 600, 1000, 2000, 4000]

def graph_factory(n: int) -> tuple:
    edges = []
    for i in range(n - 1):
        edges.append((i, i + 1))
    extras = n // 3
    for _ in range(extras):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edges.append((u, v))
    adj = _make_adj(edges, n)
    return adj, 0, n

graph_results = benchmark(
    algorithms={
        "BFS":           lambda d: bfs(d),
        "DFS Recursive": lambda d: dfs(d),
        "DFS Iterative": lambda d: dfs_iterative(d),
    },
    input_sizes=GRAPH_SIZES,
    data_factory=graph_factory,
    category="Graph Traversal",
    complexities={
        "BFS": "O(V + E)",
        "DFS Recursive": "O(V + E)",
        "DFS Iterative": "O(V + E)",
    },
    descriptions={
        "BFS": "Level-order traversal using a queue.",
        "DFS Recursive": "Depth-first via call stack; elegant but stack-limited.",
        "DFS Iterative": "Depth-first with explicit stack; no recursion limit.",
    },
    repeats=4,
)

plot_time(graph_results, title="Graph Traversal — Runtime Comparison",
          out=f"{RESULTS_DIR}/graph_time.png")
plot_combined(graph_results, title="Graph Traversal — Time vs Memory",
              out=f"{RESULTS_DIR}/graph_combined.png")
print("✓ Graph benchmarks done")


# ── Save CSV summary ───────────────────────────────────────────────────────

all_results: list[BenchmarkResult] = sort_results + search_results + graph_results

csv_path = f"{RESULTS_DIR}/summary.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["category", "algorithm", "complexity", "input_size",
                     "time_ms", "memory_kb"])
    for r in all_results:
        for size, t, m in zip(r.input_sizes, r.times_ms, r.memory_kb):
            writer.writerow([r.category, r.algorithm, r.complexity, size, t, m])

print(f"✓ Summary saved → {csv_path}")
print("\nAll benchmarks complete. Charts saved to results/")

import subprocess, os, glob

print("\nOpening charts...")
charts = sorted(glob.glob("results/*.png"))
for chart in charts:
    os.startfile(chart)   # Windows only — opens each PNG
    import time
    time.sleep(1.5)