# DSA Algorithm Benchmarker

Runtime and memory benchmarks for classic DSA algorithms : sorting, searching, and graph traversal measured across input sizes and visualized with matplotlib.

![Demo](./demo.gif)

## Charts generated

| Category        | Chart                                     |
| --------------- | ----------------------------------------- |
| Sorting         | Runtime comparison, peak memory, combined |
| Searching       | Runtime comparison, combined              |
| Graph Traversal | Runtime comparison, combined              |

## Algorithms covered

**Sorting**
| Algorithm | Complexity | Notes |
|---|---|---|
| Bubble Sort | O(n²) | Baseline for comparison |
| Selection Sort | O(n²) | Minimal swaps |
| Insertion Sort | O(n²) | Fast on nearly-sorted data |
| Merge Sort | O(n log n) | Stable, guaranteed |
| Quick Sort | O(n log n) avg | Fast in practice |
| Heap Sort | O(n log n) | In-place |
| Timsort (built-in) | O(n log n) | Python's hybrid sort |

**Searching**
| Algorithm | Complexity | Notes |
|---|---|---|
| Linear Search | O(n) | No precondition |
| Binary Search | O(log n) | Sorted array required |
| Jump Search | O(√n) | Block-based |
| Interpolation Search | O(log log n) avg | Uniform distribution |

**Graph Traversal**
| Algorithm | Complexity | Notes |
|---|---|---|
| BFS | O(V + E) | Level-order, queue-based |
| DFS Recursive | O(V + E) | Elegant; stack-limited |
| DFS Iterative | O(V + E) | No recursion limit |

## Setup

```bash
git clone https://github.com/Aaricacoding/dsa-benchmarker
cd dsa-benchmarker
pip install -r requirements.txt
python run_benchmarks.py
```

Charts saved to `results/`. Summary CSV at `results/summary.csv`.

## Project structure

```
dsa-benchmarker/
├── algorithms.py       # All algorithm implementations
├── benchmarker.py      # Timing + memory measurement engine
├── charts.py           # Matplotlib chart helpers
├── run_benchmarks.py   # Entry point — runs everything
├── requirements.txt    # matplotlib only
└── results/            # Generated charts + summary.csv
```

## Key design decisions

- Every algorithm is implemented from scratch (no `sorted()` used for sorting benchmarks)
- `tracemalloc` for peak memory tracking per run
- Each benchmark runs 3-5 times and averages results to reduce noise
- CSV output lets you do further analysis in pandas / Excel / Tableau
