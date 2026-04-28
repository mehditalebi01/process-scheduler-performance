"""
visualization.py — Visualization Module for CPU Scheduling Simulation

This module generates all visual outputs: Gantt charts, metric comparison
bar charts, per-process results tables, the evaluation dashboard, and
a normalized metric comparison chart.

All time axes are labeled with the configured time unit (t.u.) and
include explanatory footnotes about the abstract time representation.

"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from context import TIME_UNIT


# ─────────────────────────────────────────────────────────────────────
# Color Configuration
# ─────────────────────────────────────────────────────────────────────

PROCESS_COLORS = {
    "P1": "#4e79a7",
    "P2": "#4e79a7",
    "P3": "#4e79a7",
    "P4": "#4e79a7",
    "P5": "#4e79a7",
    "P6": "#4e79a7",
    "P7": "#4e79a7",
    "P8": "#4e79a7",
    "P9": "#4e79a7",
    "P10": "#4e79a7",
    "IDLE": "#4e79a7",
}

# Extended colormap for dynamic PID assignment (live scenario)
_DYNAMIC_CMAP = plt.cm.get_cmap("tab20")
_dynamic_color_cache = {}


def get_process_color(pid):
    """
    Get color for a process by PID. Uses predefined colors for P1–P10,
    and dynamically generates colors from a colormap for arbitrary PIDs
    (e.g., real system PIDs like '4832').
    """
    if pid in PROCESS_COLORS:
        return PROCESS_COLORS[pid]

    if pid not in _dynamic_color_cache:
        idx = len(_dynamic_color_cache) % 20
        _dynamic_color_cache[pid] = mcolors.to_hex(_DYNAMIC_CMAP(idx))

    return _dynamic_color_cache[pid]


# ─────────────────────────────────────────────────────────────────────
# Time Unit Footnote (added to all figures)
# ─────────────────────────────────────────────────────────────────────

TIME_FOOTNOTE = (
    f"Time is measured in abstract time units ({TIME_UNIT}). "
    "In real OS, 1 t.u. may correspond to ms or CPU cycles depending on hardware."
)


# ═══════════════════════════════════════════════════════════════════════
# 1. Gantt Chart
# ═══════════════════════════════════════════════════════════════════════

def create_gantt_figure(all_schedules, scenario_name="Selected Scenario"):
    num_algorithms = len(all_schedules)
    fig, axes = plt.subplots(
        num_algorithms, 1, figsize=(15, 3 * num_algorithms), sharex=True
    )

    if num_algorithms == 1:
        axes = [axes]

    for ax, (title, schedule) in zip(axes, all_schedules.items()):
        y = 10
        height = 6

        for pid, start, end in schedule:
            duration = end - start

            ax.broken_barh(
                [(start, duration)],
                (y, height),
                facecolors=get_process_color(pid),
                edgecolors="black",
                linewidth=1.2,
            )

            ax.text(
                start + duration / 2,
                y + height / 2,
                pid,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                color="black",
            )

            ax.text(start, y - 1.2, str(start), fontsize=8, ha="center")
            ax.text(end, y - 1.2, str(end), fontsize=8, ha="center")

        ax.set_title(f"{title} Gantt Chart", fontsize=12, fontweight="bold", pad=10)
        ax.set_yticks([])
        ax.set_ylabel("CPU", fontsize=10)
        ax.grid(True, axis="x", linestyle="--", alpha=0.4)

        total_end = max(end for _, _, end in schedule)
        ax.set_xlim(0, total_end + 1)

    axes[-1].set_xlabel(f"Time ({TIME_UNIT})", fontsize=11, fontweight="bold")

    fig.suptitle(
        f"CPU Scheduling — Gantt Charts\nScenario: {scenario_name}",
        fontsize=16,
        fontweight="bold",
    )

    # Add footnote
    fig.text(0.5, 0.01, TIME_FOOTNOTE, ha="center", fontsize=8, color="#666666", style="italic")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    return fig


# ═══════════════════════════════════════════════════════════════════════
# 2. Metric Comparison Bar Charts
# ═══════════════════════════════════════════════════════════════════════

def create_comparison_figure(results, scenario_name="Selected Scenario"):
    algorithm_names = list(results.keys())

    avg_waiting = [results[name]["avg_waiting_time"] for name in algorithm_names]
    avg_turnaround = [results[name]["avg_turnaround_time"] for name in algorithm_names]
    avg_response = [results[name]["avg_response_time"] for name in algorithm_names]

    metrics = [
        (f"Average Waiting Time ({TIME_UNIT})", avg_waiting),
        (f"Average Turnaround Time ({TIME_UNIT})", avg_turnaround),
        (f"Average Response Time ({TIME_UNIT})", avg_response),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(13, 12))

    for ax, (metric_name, values) in zip(axes, metrics):
        min_value = min(values)

        colors = []
        for value in values:
            if value == min_value:
                colors.append("#2ca02c")  # best
            else:
                colors.append("#4e79a7")

        x = np.arange(len(algorithm_names))
        bars = ax.bar(x, values, color=colors, edgecolor="black", linewidth=1.0)

        ax.set_title(metric_name, fontsize=12, fontweight="bold")
        ax.set_ylabel(f"Time ({TIME_UNIT})")
        ax.set_xticks(x)
        ax.set_xticklabels(algorithm_names, rotation=0)
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h + 0.1,
                f"{h:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
            )

    fig.suptitle(
        f"Scheduling Metrics Comparison\nScenario: {scenario_name}",
        fontsize=16,
        fontweight="bold",
    )

    fig.text(0.5, 0.01, TIME_FOOTNOTE, ha="center", fontsize=8, color="#666666", style="italic")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    return fig


# ═══════════════════════════════════════════════════════════════════════
# 3. Per-Process Results Table
# ═══════════════════════════════════════════════════════════════════════

def create_results_table_figure(all_completed, scenario_name="Selected Scenario"):
    num_algorithms = len(all_completed)
    fig, axes = plt.subplots(num_algorithms, 1, figsize=(16, 3 * num_algorithms))

    if num_algorithms == 1:
        axes = [axes]

    for ax, (name, completed) in zip(axes, all_completed.items()):
        ax.axis("off")

        columns = [
            "PID",
            f"Arrival ({TIME_UNIT})",
            f"Burst ({TIME_UNIT})",
            f"Start ({TIME_UNIT})",
            f"Completion ({TIME_UNIT})",
            f"Waiting ({TIME_UNIT})",
            f"Turnaround ({TIME_UNIT})",
            f"Response ({TIME_UNIT})",
        ]

        table_data = []
        completed_sorted = sorted(completed, key=lambda x: x["pid"])

        for p in completed_sorted:
            table_data.append(
                [
                    p["pid"],
                    p["arrival_time"],
                    p["burst_time"],
                    p["start_time"],
                    p["completion_time"],
                    p["waiting_time"],
                    p["turnaround_time"],
                    p["response_time"],
                ]
            )

        table = ax.table(
            cellText=table_data, colLabels=columns, cellLoc="center", loc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)

        for (row, col), cell in table.get_celld().items():
            cell.set_edgecolor("black")
            cell.set_linewidth(0.8)
            if row == 0:
                cell.set_text_props(weight="bold", color="black")
                cell.set_facecolor("#d9eaf7")
            else:
                cell.set_facecolor("#f8f8f8")

        ax.set_title(
            f"{name} - Process Results", fontsize=12, fontweight="bold", pad=10
        )

    fig.suptitle(
        f"Per-Process Detailed Results\nScenario: {scenario_name}",
        fontsize=16,
        fontweight="bold",
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    return fig


# ═══════════════════════════════════════════════════════════════════════
# 4. Dashboard
# ═══════════════════════════════════════════════════════════════════════

def create_dashboard_figure(results, scenario_name="Selected Scenario"):
    algorithm_names = list(results.keys())

    best_waiting = min(results.items(), key=lambda x: x[1]["avg_waiting_time"])
    best_turnaround = min(results.items(), key=lambda x: x[1]["avg_turnaround_time"])
    best_response = min(results.items(), key=lambda x: x[1]["avg_response_time"])
    best_throughput = max(results.items(), key=lambda x: x[1]["throughput"])

    throughput_values = [results[name]["throughput"] for name in algorithm_names]
    x = np.arange(len(algorithm_names))

    fig, axes = plt.subplots(2, 1, figsize=(13, 9))

    axes[0].axis("off")
    summary_text = (
        f"Scenario: {scenario_name}\n\n"
        f"Best Average Waiting Time    : {best_waiting[0]} ({best_waiting[1]['avg_waiting_time']:.2f} {TIME_UNIT})\n"
        f"Best Average Turnaround Time : {best_turnaround[0]} ({best_turnaround[1]['avg_turnaround_time']:.2f} {TIME_UNIT})\n"
        f"Best Average Response Time   : {best_response[0]} ({best_response[1]['avg_response_time']:.2f} {TIME_UNIT})\n"
        f"Best Throughput             : {best_throughput[0]} ({best_throughput[1]['throughput']:.2f} proc/{TIME_UNIT})\n"
    )

    axes[0].text(
        0.02,
        0.95,
        summary_text,
        transform=axes[0].transAxes,
        fontsize=13,
        va="top",
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.8", edgecolor="black", facecolor="#f5f5f5"),
    )

    bars = axes[1].bar(x, throughput_values, color="#9c755f", edgecolor="black")
    axes[1].set_title("Throughput Comparison", fontsize=12, fontweight="bold")
    axes[1].set_ylabel(f"Throughput (proc/{TIME_UNIT})")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(algorithm_names)
    axes[1].grid(True, axis="y", linestyle="--", alpha=0.4)

    for bar in bars:
        h = bar.get_height()
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.002,
            f"{h:.2f}",
            ha="center",
            fontsize=9,
            fontweight="bold",
        )

    fig.suptitle("Scheduling Dashboard", fontsize=16, fontweight="bold")
    fig.text(0.5, 0.01, TIME_FOOTNOTE, ha="center", fontsize=8, color="#666666", style="italic")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    return fig


# ═══════════════════════════════════════════════════════════════════════
# 5. Normalized Metric Comparison (NEW)
# ═══════════════════════════════════════════════════════════════════════

def create_normalized_comparison_figure(results, scenario_name="Selected Scenario"):
    """
    Create a normalized (0–1 scale) comparison chart for all metrics.
    Uses min-max normalization:  normalized = (value - min) / (max - min)
    Lower is better for time metrics; the normalization preserves this.
    """
    algorithm_names = list(results.keys())
    n_alg = len(algorithm_names)

    metric_keys = ["avg_waiting_time", "avg_turnaround_time", "avg_response_time"]
    metric_labels = [
        "Avg Waiting Time",
        "Avg Turnaround Time",
        "Avg Response Time",
    ]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7),
                             gridspec_kw={'width_ratios': [2, 1]})

    # ── Left panel: Grouped bar chart ──
    x = np.arange(n_alg)
    width = 0.25
    offsets = [-width, 0, width]
    colors = ["#4e79a7", "#f28e2b", "#e15759"]

    for i, (key, label) in enumerate(zip(metric_keys, metric_labels)):
        raw_values = [results[name][key] for name in algorithm_names]
        min_val = min(raw_values)
        max_val = max(raw_values)
        if max_val - min_val > 0:
            normalized = [(v - min_val) / (max_val - min_val) for v in raw_values]
        else:
            normalized = [0.0] * n_alg

        bars = axes[0].bar(x + offsets[i], normalized, width,
                           label=label, color=colors[i], edgecolor="black", linewidth=0.8)

        for bar, norm_val, raw_val in zip(bars, normalized, raw_values):
            axes[0].text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.02,
                f"{norm_val:.2f}\n({raw_val:.1f})",
                ha="center", va="bottom", fontsize=7, fontweight="bold"
            )

    axes[0].set_title("Normalized Metric Comparison (0–1 Scale)", fontsize=13, fontweight="bold")
    axes[0].set_ylabel("Normalized Value (0 = best, 1 = worst)")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(algorithm_names)
    axes[0].set_ylim(0, 1.35)
    axes[0].legend(loc="upper right", fontsize=9)
    axes[0].grid(True, axis="y", linestyle="--", alpha=0.4)

    # ── Right panel: Normalization formula explanation ──
    axes[1].axis("off")
    formula_text = (
        "Min-Max Normalization\n"
        "─────────────────────\n\n"
        r"$x_{norm} = \frac{x - x_{min}}{x_{max} - x_{min}}$"
        "\n\n"
        "Scale: [0, 1]\n"
        "  0 = best performance\n"
        "  1 = worst performance\n\n"
        "This allows direct visual\n"
        "comparison across metrics\n"
        "with different scales.\n\n"
        "Raw values shown in\n"
        "parentheses on each bar."
    )
    axes[1].text(
        0.1, 0.85, formula_text,
        transform=axes[1].transAxes,
        fontsize=11, va="top", family="monospace",
        bbox=dict(boxstyle="round,pad=0.8", edgecolor="#2c3e50", facecolor="#f0f4f8")
    )

    fig.suptitle(
        f"Normalized Performance Comparison\nScenario: {scenario_name}",
        fontsize=16, fontweight="bold"
    )
    fig.text(0.5, 0.01, TIME_FOOTNOTE, ha="center", fontsize=8, color="#666666", style="italic")
    plt.tight_layout(rect=[0, 0.03, 1, 0.93])

    return fig
