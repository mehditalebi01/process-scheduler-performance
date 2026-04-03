import matplotlib.pyplot as plt
import numpy as np


def create_gantt_figure(all_schedules):
    """
    all_schedules = {
        "FCFS": schedule,
        "SJF": schedule,
        ...
    }
    """
    num_algorithms = len(all_schedules)
    fig, axes = plt.subplots(num_algorithms, 1, figsize=(14, 2.8 * num_algorithms), sharex=True)

    if num_algorithms == 1:
        axes = [axes]

    for ax, (title, schedule) in zip(axes, all_schedules.items()):
        y_position = 10
        height = 6

        for i, (pid, start, end) in enumerate(schedule):
            duration = end - start

            ax.broken_barh(
                [(start, duration)],
                (y_position, height),
                facecolors=f"C{i % 10}",
                edgecolors="black",
                linewidth=1.0
            )

            ax.text(
                start + duration / 2,
                y_position + height / 2,
                pid,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold"
            )

        ax.set_title(f"{title} - Gantt Chart", fontsize=12, fontweight="bold")
        ax.set_ylabel("CPU")
        ax.set_yticks([])
        ax.grid(True, axis="x", linestyle="--", alpha=0.5)

    axes[-1].set_xlabel("Time")
    fig.suptitle("CPU Scheduling - All Gantt Charts", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    return fig


def create_comparison_figure(results):
    """
    results = {
        "FCFS": {"avg_waiting_time": ..., "avg_turnaround_time": ..., ...},
        ...
    }
    """
    algorithm_names = list(results.keys())

    avg_waiting = [results[name]["avg_waiting_time"] for name in algorithm_names]
    avg_turnaround = [results[name]["avg_turnaround_time"] for name in algorithm_names]
    avg_response = [results[name]["avg_response_time"] for name in algorithm_names]

    x = np.arange(len(algorithm_names))
    width = 0.22

    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    # Waiting Time
    bars1 = axes[0].bar(x, avg_waiting, width=0.6, edgecolor="black")
    axes[0].set_title("Average Waiting Time", fontweight="bold")
    axes[0].set_ylabel("Time")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(algorithm_names)
    axes[0].grid(True, axis="y", linestyle="--", alpha=0.5)
    for bar in bars1:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, h + 0.1, f"{h:.2f}", ha="center", fontsize=9)

    # Turnaround Time
    bars2 = axes[1].bar(x, avg_turnaround, width=0.6, edgecolor="black")
    axes[1].set_title("Average Turnaround Time", fontweight="bold")
    axes[1].set_ylabel("Time")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(algorithm_names)
    axes[1].grid(True, axis="y", linestyle="--", alpha=0.5)
    for bar in bars2:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.1, f"{h:.2f}", ha="center", fontsize=9)

    # Response Time
    bars3 = axes[2].bar(x, avg_response, width=0.6, edgecolor="black")
    axes[2].set_title("Average Response Time", fontweight="bold")
    axes[2].set_ylabel("Time")
    axes[2].set_xticks(x)
    axes[2].set_xticklabels(algorithm_names)
    axes[2].grid(True, axis="y", linestyle="--", alpha=0.5)
    for bar in bars3:
        h = bar.get_height()
        axes[2].text(bar.get_x() + bar.get_width()/2, h + 0.1, f"{h:.2f}", ha="center", fontsize=9)

    fig.suptitle("Scheduling Algorithms - Metrics Comparison", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    return fig


def create_results_table_figure(all_completed):
    """
    all_completed = {
        "FCFS": completed_list,
        "SJF": completed_list,
        ...
    }
    """
    num_algorithms = len(all_completed)
    fig, axes = plt.subplots(num_algorithms, 1, figsize=(15, 2.8 * num_algorithms))

    if num_algorithms == 1:
        axes = [axes]

    for ax, (name, completed) in zip(axes, all_completed.items()):
        ax.axis("off")

        columns = ["PID", "Arrival", "Burst", "Start", "Completion", "Waiting", "Turnaround", "Response"]
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
            loc="center",
            cellLoc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.4)
        ax.set_title(f"{name} - Process Results", fontsize=12, fontweight="bold", pad=10)

    fig.suptitle("Per-Process Results", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    return fig


def create_dashboard_figure(results):
    algorithm_names = list(results.keys())

    best_waiting = min(results.items(), key=lambda x: x[1]["avg_waiting_time"])
    best_turnaround = min(results.items(), key=lambda x: x[1]["avg_turnaround_time"])
    best_response = min(results.items(), key=lambda x: x[1]["avg_response_time"])
    best_throughput = max(results.items(), key=lambda x: x[1]["throughput"])

    throughput_values = [results[name]["throughput"] for name in algorithm_names]
    x = np.arange(len(algorithm_names))

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # text summary
    axes[0].axis("off")
    summary_text = (
        "Scheduling Summary\n\n"
        f"Best Average Waiting Time   : {best_waiting[0]} ({best_waiting[1]['avg_waiting_time']:.2f})\n"
        f"Best Average Turnaround Time: {best_turnaround[0]} ({best_turnaround[1]['avg_turnaround_time']:.2f})\n"
        f"Best Average Response Time  : {best_response[0]} ({best_response[1]['avg_response_time']:.2f})\n"
        f"Best Throughput            : {best_throughput[0]} ({best_throughput[1]['throughput']:.2f})\n"
    )
    axes[0].text(
        0.02, 0.95, summary_text,
        transform=axes[0].transAxes,
        fontsize=13,
        va="top",
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.6", edgecolor="black", facecolor="#f5f5f5")
    )

    # throughput chart
    bars = axes[1].bar(x, throughput_values, width=0.6, edgecolor="black")
    axes[1].set_title("Throughput Comparison", fontweight="bold")
    axes[1].set_ylabel("Throughput")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(algorithm_names)
    axes[1].grid(True, axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        h = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.005, f"{h:.2f}", ha="center", fontsize=9)

    fig.suptitle("Dashboard", fontsize=16, fontweight="bold")
    plt.tight_layout(rect=[0, 0, 1, 0.97])

    return fig

    