"""
main.py — CPU Scheduling Performance Simulation

Interactive Command-Line Interface for selecting workload scenarios
and running all five scheduling algorithms with comprehensive output.

This simulation produces:
    1. Formal metric definitions and mathematical formulas
    2. Test bed context and limitations
    3. Per-process results tables
    4. Gantt charts for all algorithms
    5. Metric comparison bar charts (raw and normalized)
    6. Evaluation dashboard
    7. Pseudocode for all algorithms
    8. Result analysis with motivation ("WHY" explanations)

Authors:
    Mehdi Talebikhatir (ID: 558948)
    Benyamin Baharizadeh (ID: 560587)

Course: Data Analysis (L-31) — Operating Systems
Professors: Prof. M. Giacobbe, Prof. M. Fazio
"""

import matplotlib.pyplot as plt
from schedulers import fcfs, sjf, round_robin, priority_scheduling, srtf, create_pseudocode_figure
from metrics import calculate_averages
from visualization import (
    create_gantt_figure,
    create_comparison_figure,
    create_results_table_figure,
    create_dashboard_figure,
    create_normalized_comparison_figure,
)
from formulas import print_metric_definitions, create_formulas_figure
from context import print_testbed_context, create_context_figure
from analysis import generate_analysis, create_analysis_figure


# ═══════════════════════════════════════════════════════════════════════
# Interactive Menu
# ═══════════════════════════════════════════════════════════════════════

print("=" * 60)
print("  CPU SCHEDULING ALGORITHMS PERFORMANCE SIMULATION")
print("=" * 60)

sampledata = input(
    "\nSelect a workload scenario:\n"
    "  1. Basic              (baseline test)\n"
    "  2. Convoy Effect      (FCFS weakness demo)\n"
    "  3. RR Friendly        (time-sharing favored)\n"
    "  4. Priority Case      (priority inversion test)\n"
    "  5. SRTF Case          (preemption showcase)\n"
    "  6. Presentation       (complex mixed workload)\n"
    "  7. Live System        (real OS processes)\n"
    ">>> "
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
elif sampledata == "7":
    from sample_data import scenario_live_system
    processes = scenario_live_system()
    scenario_name = "Live System"
else:
    from sample_data import scenario_basic
    print("Invalid choice. Defaulting to Basic scenario.")
    processes = scenario_basic()
    scenario_name = "Basic"


# ═══════════════════════════════════════════════════════════════════════
# Phase 1: Print Formal Context
# ═══════════════════════════════════════════════════════════════════════

print_metric_definitions()
print_testbed_context()

# Print the input process set
print("\n" + "=" * 70)
print(f"INPUT PROCESS SET -- Scenario: {scenario_name}")
print("=" * 70)
print(f"{'PID':<20s} {'Arrival (t.u.)':<15s} {'Burst (t.u.)':<15s} {'Priority':<10s}")
print("-" * 60)
for p in processes:
    print(f"{p.pid:<20s} {p.arrival_time:<15d} {p.burst_time:<15d} {p.priority:<10d}")
print("=" * 70)


# ═══════════════════════════════════════════════════════════════════════
# Phase 2: Run All Algorithms
# ═══════════════════════════════════════════════════════════════════════

def print_results(completed, averages):
    print("\nProcess Results:")
    for p in completed:
        print(
            f"  {p['pid']}: "
            f"Waiting={p['waiting_time']} t.u., "
            f"Turnaround={p['turnaround_time']} t.u., "
            f"Response={p['response_time']} t.u."
        )

    print("\nAverages:")
    print(f"  Average Waiting Time    : {averages['avg_waiting_time']:.2f} t.u.")
    print(f"  Average Turnaround Time : {averages['avg_turnaround_time']:.2f} t.u.")
    print(f"  Average Response Time   : {averages['avg_response_time']:.2f} t.u.")
    print(f"  Throughput              : {averages['throughput']:.4f} proc/t.u.")


def run_algorithm(name, algorithm, processes):
    print(f"\n{'=' * 50}")
    print(f"  {name} Scheduling")
    print(f"{'=' * 50}")

    schedule, completed = algorithm(processes)
    averages = calculate_averages(completed)

    print_results(completed, averages)

    print("\n  Gantt Data:")
    for item in schedule:
        print(f"    {item}")

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

    # ── Phase 3: Generate Analysis ──
    generate_analysis(comparison_results, scenario_name)

    # ── Phase 4: Generate All Figures ──
    print("\n" + "=" * 70)
    print("GENERATING VISUAL OUTPUT...")
    print("=" * 70)

    # Figure 1: Metric definitions & formulas
    create_formulas_figure()

    # Figure 2: Test bed context & limitations
    create_context_figure()

    # Figure 3: Pseudocode for all algorithms
    create_pseudocode_figure()

    # Figure 4: Per-process results tables
    create_results_table_figure(all_completed, scenario_name)

    # Figure 5: Metric comparison bar charts (raw values)
    create_comparison_figure(comparison_results, scenario_name)

    # Figure 6: Normalized metric comparison (0–1 scale)
    create_normalized_comparison_figure(comparison_results, scenario_name)

    # Figure 7: Gantt charts
    create_gantt_figure(all_schedules, scenario_name)

    # Figure 8: Evaluation dashboard
    create_dashboard_figure(comparison_results, scenario_name)

    # Figure 9: Analysis & motivation
    create_analysis_figure(comparison_results, scenario_name)

    print("\nAll figures generated. Displaying...")
    plt.show()


if __name__ == "__main__":
    main()
