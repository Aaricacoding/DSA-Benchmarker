"""
charts.py — matplotlib chart helpers for benchmark results.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from benchmarker import BenchmarkResult

PALETTE = [
    "#4f8ef7", "#3ecf8e", "#f4a261", "#a78bfa",
    "#f56565", "#fbbf24", "#38bdf8", "#fb7185",
]

plt.rcParams.update({
    "figure.facecolor": "#0d0f14",
    "axes.facecolor":   "#151820",
    "axes.edgecolor":   "#232733",
    "axes.labelcolor":  "#9ca3af",
    "xtick.color":      "#6b7080",
    "ytick.color":      "#6b7080",
    "grid.color":       "#1f2433",
    "grid.linewidth":   0.8,
    "text.color":       "#e8eaf0",
    "font.family":      "sans-serif",
    "axes.spines.top":  False,
    "axes.spines.right": False,
    "axes.grid":        True,
    "legend.facecolor": "#151820",
    "legend.edgecolor": "#232733",
    "legend.fontsize":  9,
})


def _complexity_label(r: BenchmarkResult) -> str:
    return f"{r.algorithm}  [{r.complexity}]"


def plot_time(results: list[BenchmarkResult], title: str, out: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for i, r in enumerate(results):
        color = PALETTE[i % len(PALETTE)]
        ax.plot(r.input_sizes, r.times_ms,
                marker="o", markersize=5, linewidth=2,
                color=color, label=_complexity_label(r))

    ax.set_title(title, fontsize=13, fontweight="bold", pad=14, color="#e8eaf0")
    ax.set_xlabel("Input Size (n)", fontsize=10)
    ax.set_ylabel("Time (ms)", fontsize=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.legend(loc="upper left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_memory(results: list[BenchmarkResult], title: str, out: str) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    x = list(range(len(results)))
    bars = ax.bar(x, [r.memory_kb[-1] for r in results],
                  color=[PALETTE[i % len(PALETTE)] for i in x],
                  alpha=0.85, width=0.6, zorder=3)

    for bar, r in zip(bars, results):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                f"{bar.get_height():.1f} KB",
                ha="center", va="bottom", fontsize=8.5, color="#9ca3af")

    ax.set_xticks(x)
    ax.set_xticklabels([r.algorithm for r in results], rotation=18, ha="right", fontsize=9)
    ax.set_title(title, fontsize=13, fontweight="bold", pad=14, color="#e8eaf0")
    ax.set_ylabel("Peak Memory (KB)", fontsize=10)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_combined(results: list[BenchmarkResult], title: str, out: str) -> None:
    """Side-by-side: time line chart + memory bar chart."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # Left: time
    for i, r in enumerate(results):
        color = PALETTE[i % len(PALETTE)]
        ax1.plot(r.input_sizes, r.times_ms,
                 marker="o", markersize=4, linewidth=2,
                 color=color, label=_complexity_label(r))
    ax1.set_title("Runtime", fontsize=11, fontweight="bold", color="#e8eaf0")
    ax1.set_xlabel("Input Size (n)", fontsize=9)
    ax1.set_ylabel("Time (ms)", fontsize=9)
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax1.legend(fontsize=8, framealpha=0.9)

    # Right: peak memory at largest n
    x = list(range(len(results)))
    bars = ax2.bar(x, [r.memory_kb[-1] for r in results],
                   color=[PALETTE[i % len(PALETTE)] for i in x],
                   alpha=0.85, width=0.55, zorder=3)
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.3,
                 f"{bar.get_height():.1f}",
                 ha="center", va="bottom", fontsize=8, color="#9ca3af")
    ax2.set_xticks(x)
    ax2.set_xticklabels([r.algorithm for r in results], rotation=20, ha="right", fontsize=8)
    ax2.set_title(f"Peak Memory @ n={results[0].input_sizes[-1]:,}", fontsize=11,
                  fontweight="bold", color="#e8eaf0")
    ax2.set_ylabel("Memory (KB)", fontsize=9)

    fig.suptitle(title, fontsize=13, fontweight="bold", color="#e8eaf0", y=1.01)
    fig.tight_layout()
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
