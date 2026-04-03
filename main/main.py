print("******** welcome to process scheduler performance simulation ********")

sampledata = input(
    "enter sample data:\n"
    "1. basic\n"
    "2. convoy effect\n"
    "3. rr friendly\n"
    "4. priority case\n"
    "5. srtf case\n"
    "6. presentation\n"
    ">>>"
)

if sampledata == "1":
    from sample_data import scenario_basic
    processes = scenario_basic()
    scenario_name = "Basic"
elif sampledata == "2":
    from sample_data import scenario_convoy_effect
    processes = scenario_convoy_effect()
    scenario_name = "Convoy Effect"
elif sampledata == "3":
    from sample_data import scenario_rr_friendly
    processes = scenario_rr_friendly()
    scenario_name = "RR Friendly"
elif sampledata == "4":
    from sample_data import scenario_priority_case
    processes = scenario_priority_case()
    scenario_name = "Priority Case"
elif sampledata == "5":
    from sample_data import scenario_srtf_case
    processes = scenario_srtf_case()
    scenario_name = "SRTF Case"
elif sampledata == "6":
    from sample_data import scenario_presentation
    processes = scenario_presentation()
    scenario_name = "Presentation"
else:
    from sample_data import scenario_basic
    print("invalid choice, basic scenario selected.")
    processes = scenario_basic()
    scenario_name = "Basic"



import matplotlib.pyplot as plt
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