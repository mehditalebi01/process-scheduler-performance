import matplotlib.pyplot as plt

from sample_data import get_sample_processes
from schedulers import fcfs, sjf, round_robin, priority_scheduling, srtf
from metrics import calculate_averages
from visualization import (
    create_gantt_figure,
    create_comparison_figure,
    create_results_table_figure,
    create_dashboard_figure
)


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

    return schedule, completed, averages


def main():
    processes = get_sample_processes()

    algorithms = {
        "FCFS": fcfs,
        "SJF": sjf,
        "RR (q=2)": lambda p: round_robin(p, quantum=2),
        "Priority": priority_scheduling,
        "SRTF": srtf,
    }

    all_schedules = {}
    all_completed = {}
    comparison_results = {}

    for name, algorithm in algorithms.items():
        schedule, completed, averages = run_algorithm(name, algorithm, processes)
        all_schedules[name] = schedule
        all_completed[name] = completed
        comparison_results[name] = averages

    create_gantt_figure(all_schedules)
    create_comparison_figure(comparison_results)
    create_results_table_figure(all_completed)
    create_dashboard_figure(comparison_results)


    plt.show()


if __name__ == "__main__":
    main()  