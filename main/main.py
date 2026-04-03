from sample_data import get_sample_processes
from schedulers import fcfs, sjf, round_robin, priority_scheduling, srtf
from metrics import calculate_averages
from visualization import plot_gantt_chart, plot_comparison_chart


def print_results(completed, averages):
    print("\nProcess Results:")
    for p in completed:
        print(
            f'{p["pid"]}: '
            f'Waiting={p["waiting_time"]}, '
            f'Turnaround={p["turnaround_time"]}, '
            f'Response={p["response_time"]}'
        )

    print("\nAverages:")
    print(f'Average Waiting Time: {averages["avg_waiting_time"]:.2f}')
    print(f'Average Turnaround Time: {averages["avg_turnaround_time"]:.2f}')
    print(f'Average Response Time: {averages["avg_response_time"]:.2f}')
    print(f'Throughput: {averages["throughput"]:.2f}')


def run_algorithm(name, algorithm, processes):
    print(f"\n{'=' * 40}")
    print(f"{name} Scheduling")
    print(f"{'=' * 40}")

    schedule, completed = algorithm(processes)
    averages = calculate_averages(completed)

    print_results(completed, averages)

    print("\nGantt Data:")
    for item in schedule:
        print(item)

    plot_gantt_chart(schedule, title=f"{name} Gantt Chart")

    return averages


def main():
    processes = get_sample_processes()

    comparison_results = {}

    comparison_results["FCFS"] = run_algorithm("FCFS", fcfs, processes)
    comparison_results["SJF"] = run_algorithm("SJF", sjf, processes)
    comparison_results["RR (q=2)"] = run_algorithm(
        "Round Robin (q=2)",
        lambda p: round_robin(p, quantum=2),
        processes
    )
    comparison_results["Priority"] = run_algorithm("Priority", priority_scheduling, processes)
    comparison_results["SRTF"] = run_algorithm("SRTF", srtf, processes)

    plot_comparison_chart(comparison_results)


if __name__ == "__main__":
    main()

