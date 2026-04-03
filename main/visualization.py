import matplotlib.pyplot as plt


def plot_gantt_chart(schedule, title="Gantt Chart"):
    fig, ax = plt.subplots(figsize=(12, 3))

    y_position = 10
    height = 4

    for pid, start, end in schedule:
        duration = end - start
        ax.broken_barh([(start, duration)], (y_position, height))
        ax.text(
            start + duration / 2,
            y_position + height / 2,
            pid,
            ha="center",
            va="center"
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("CPU")
    ax.set_title(title)
    ax.set_yticks([y_position + height / 2])
    ax.set_yticklabels(["Execution"])
    ax.grid(True)

    plt.tight_layout()
    plt.show()


def plot_comparison_chart(results):
    algorithm_names = list(results.keys())

    avg_waiting = [results[name]["avg_waiting_time"] for name in algorithm_names]
    avg_turnaround = [results[name]["avg_turnaround_time"] for name in algorithm_names]
    avg_response = [results[name]["avg_response_time"] for name in algorithm_names]

    plt.figure(figsize=(10, 5))
    plt.bar(algorithm_names, avg_waiting)
    plt.xlabel("Algorithms")
    plt.ylabel("Average Waiting Time")
    plt.title("Comparison of Average Waiting Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.bar(algorithm_names, avg_turnaround)
    plt.xlabel("Algorithms")
    plt.ylabel("Average Turnaround Time")
    plt.title("Comparison of Average Turnaround Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.bar(algorithm_names, avg_response)
    plt.xlabel("Algorithms")
    plt.ylabel("Average Response Time")
    plt.title("Comparison of Average Response Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    