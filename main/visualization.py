import matplotlib.pyplot as plt
import numpy as np


PROCESS_COLORS = {
    "P1": "#4e79a7",
    "P2": "#f28e2b",
    "P3": "#e15759",
    "P4": "#76b7b2",
    "P5": "#59a14f",
    "P6": "#edc948",
    "P7": "#b07aa1",
    "P8": "#ff9da7",
    "P9": "#9c755f",
    "P10": "#bab0ab",
    "IDLE": "#d3d3d3"
}


def get_process_color(pid):
    return PROCESS_COLORS.get(pid, "#999999")


def create_gantt_figure(all_schedules, scenario_name="Selected Scenario"):
    num_algorithms = len(all_schedules)
    fig, axes = plt.subplots(
        num_algorithms, 1,
        figsize=(15, 3 * num_algorithms),
        sharex=True
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
                linewidth=1.2
            )

            ax.text(
                start + duration / 2,
                y + height / 2,
                pid,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                color="black"
            )

            ax.text(start, y - 1.2, str(start), fontsize=8, ha="center")
            ax.text(end, y - 1.2, str(end), fontsize=8, ha="center")

        ax.set_title(f"{title} Gantt Chart", fontsize=12, fontweight="bold", pad=10)
        ax.set_yticks([])
        ax.set_ylabel("CPU", fontsize=10)
        ax.grid(True, axis="x", linestyle="--", alpha=0.4)

        total_end = max(end for _, _, end in schedule)
        ax.set_xlim(0, total_end + 1)

    axes[-1].set_xlabel("Time", fontsize=11, fontweight="bold")

    fig.suptitle(
        f"CPU Scheduling - Gantt Charts\nScenario: {scenario_name}",
        fontsize=16,
        fontweight="bold"
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    return fig


def create_comparison_figure(results, scenario_name="Selected Scenario"):
    algorithm_names = list(results.keys())

    avg_waiting = [results[name]["avg_waiting_time"] for name in algorithm_names]
    avg_turnaround = [results[name]["avg_turnaround_time"] for name in algorithm_names]
    avg_response = [results[name]["avg_response_time"] for name in algorithm_names]

    metrics = [
        ("Average Waiting Time", avg_waiting),
        ("Average Turnaround Time", avg_turnaround),
        ("Average Response Time", avg_response),
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
        ax.set_ylabel("Time")
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
                fontweight="bold"
            )

    fig.suptitle(
        f"Scheduling Metrics Comparison\nScenario: {scenario_name}",
        fontsize=16,
        fontweight="bold"
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    return fig


def create_results_table_figure(all_completed, scenario_name="Selected Scenario"):
    num_algorithms = len(all_completed)
    fig, axes = plt.subplots(num_algorithms, 1, figsize=(16, 3 * num_algorithms))

    if num_algorithms == 1:
        axes = [axes]

    for ax, (name, completed) in zip(axes, all_completed.items()):
        ax.axis("off")

        columns = [
            "PID", "Arrival", "Burst", "Start",
            "Completion", "Waiting", "Turnaround", "Response"
        ]

        table_data = []
        completed_sorted = sorted(completed, key=lambda x: x["pid"])

        for p in completed_sorted:
            table_data.append([
                p["pid"],
                p["arrival_time"],
                p["burst_time"],
                p["start_time"],
                p["completion_time"],
                p["waiting_time"],
                p["turnaround_time"],
                p["response_time"],
            ])

        table = ax.table(
            cellText=table_data,
            colLabels=columns,
            cellLoc="center",
            loc="center"
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

        ax.set_title(f"{name} - Process Results", fontsize=12, fontweight="bold", pad=10)

    fig.suptitle(
        f"Per-Process Detailed Results\nScenario: {scenario_name}",
        fontsize=16,
        fontweight="bold"
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    return fig


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
        f"Best Average Waiting Time    : {best_waiting[0]} ({best_waiting[1]['avg_waiting_time']:.2f})\n"
        f"Best Average Turnaround Time : {best_turnaround[0]} ({best_turnaround[1]['avg_turnaround_time']:.2f})\n"
        f"Best Average Response Time   : {best_response[0]} ({best_response[1]['avg_response_time']:.2f})\n"
        f"Best Throughput             : {best_throughput[0]} ({best_throughput[1]['throughput']:.2f})\n"
    )

    axes[0].text(
        0.02, 0.95, summary_text,
        transform=axes[0].transAxes,
        fontsize=13,
        va="top",
        family="monospace",
        bbox=dict(
            boxstyle="round,pad=0.8",
            edgecolor="black",
            facecolor="#f5f5f5"
        )
    )

    bars = axes[1].bar(x, throughput_values, color="#9c755f", edgecolor="black")
    axes[1].set_title("Throughput Comparison", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Throughput")
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
            fontweight="bold"
        )

    fig.suptitle("Scheduling Dashboard", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    return fig

    