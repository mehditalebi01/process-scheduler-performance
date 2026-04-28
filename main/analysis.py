"""
analysis.py — Result Analysis, Motivation, and Throughput Discussion

This module generates textual and visual analysis explaining WHY each
algorithm performed the way it did for a given scenario. It identifies
the best/worst algorithms, explains the underlying mechanics, and
discusses phenomena like the convoy effect, starvation, and throughput.

"""

import matplotlib.pyplot as plt
import textwrap


# ─────────────────────────────────────────────────────────────────────
# Algorithm characteristics (used for generating explanations)
# ─────────────────────────────────────────────────────────────────────

ALGORITHM_TRAITS = {
    "FCFS": {
        "type": "Non-preemptive",
        "strength": "Simple, fair in arrival order, zero starvation",
        "weakness": "Convoy effect -- short processes stuck behind long ones",
        "why_best_wt": (
            "FCFS achieves the lowest average waiting time when processes arrive "
            "in increasing burst-time order, eliminating the convoy effect."
        ),
        "why_worst_wt": (
            "FCFS produces high waiting times due to the convoy effect: "
            "a long-burst process arriving early forces all subsequent short "
            "processes to wait, inflating the average waiting time."
        ),
        "why_best_rt": (
            "FCFS achieves low response time when burst times are small and "
            "arrivals are spread out, since each process starts immediately."
        ),
        "why_worst_rt": (
            "In FCFS, response time degrades when many processes arrive close "
            "together -- later arrivals must wait for all preceding bursts."
        ),
    },
    "SJF": {
        "type": "Non-preemptive",
        "strength": "Provably optimal average waiting time for non-preemptive scheduling",
        "weakness": "Starvation of long processes; requires burst-time knowledge",
        "why_best_wt": (
            "SJF is mathematically proven to minimize average waiting time among "
            "non-preemptive algorithms (Silberschatz et al., Ch. 5.3.2). By always "
            "selecting the shortest available job, it minimizes the cumulative "
            "waiting of all remaining processes."
        ),
        "why_worst_wt": (
            "SJF rarely produces the worst waiting time. If it does, the workload "
            "likely has uniform burst times, neutralizing SJF's advantage."
        ),
        "why_best_rt": (
            "SJF achieves good response time when short jobs arrive early, "
            "as they are scheduled immediately."
        ),
        "why_worst_rt": (
            "Long processes in SJF may experience very high response times "
            "if short processes continually arrive, causing starvation."
        ),
    },
    "RR (q=2)": {
        "type": "Preemptive (time-sharing)",
        "strength": "Excellent response time; fair CPU distribution via time slicing",
        "weakness": "Higher average waiting time due to context switches; quantum-sensitive",
        "why_best_wt": (
            "Round Robin achieves competitive waiting times when all processes "
            "have similar burst times, as the time-slicing distributes wait evenly."
        ),
        "why_worst_wt": (
            "RR produces higher waiting times because every process is repeatedly "
            "preempted and re-queued, accumulating wait time across multiple quanta. "
            "The small quantum (q=2) amplifies this effect."
        ),
        "why_best_rt": (
            "Round Robin excels at response time because every process receives "
            "its first CPU quantum within at most n*q time units of arrival. "
            "This makes it ideal for interactive/time-sharing systems where user "
            "responsiveness is critical (Tanenbaum, Ch. 2.4.2)."
        ),
        "why_worst_rt": (
            "RR response time degrades only when many processes arrive simultaneously "
            "and the queue becomes very long."
        ),
    },
    "Priority": {
        "type": "Non-preemptive",
        "strength": "Respects task importance; suitable for real-time systems",
        "weakness": "Starvation of low-priority processes; priority inversion risk",
        "why_best_wt": (
            "Priority scheduling achieves low waiting time when high-priority "
            "processes also have short burst times, combining priority with efficiency."
        ),
        "why_worst_wt": (
            "Priority scheduling can produce poor waiting times when priority "
            "ordering conflicts with burst-time ordering -- a high-priority, "
            "long-burst process forces shorter lower-priority processes to wait."
        ),
        "why_best_rt": (
            "High-priority processes get immediate CPU access, giving them "
            "excellent response times."
        ),
        "why_worst_rt": (
            "Low-priority processes may experience indefinite postponement "
            "(starvation), resulting in very poor response times."
        ),
    },
    "SRTF": {
        "type": "Preemptive",
        "strength": "Optimal average waiting time (preemptive); highly responsive",
        "weakness": "Frequent context switches; starvation of long processes",
        "why_best_wt": (
            "SRTF is the preemptive counterpart of SJF and is provably optimal "
            "for minimizing average waiting time across all scheduling algorithms "
            "(Silberschatz et al., Ch. 5.3.4). When a new shorter process arrives, "
            "SRTF immediately preempts the current one, ensuring no process waits "
            "unnecessarily behind a longer one."
        ),
        "why_worst_wt": (
            "SRTF very rarely produces the worst waiting time. This would only "
            "occur in degenerate cases with uniform burst times where preemption "
            "overhead (not modeled here) outweighs the benefit."
        ),
        "why_best_rt": (
            "SRTF provides excellent response times because short processes "
            "arriving mid-execution can preempt longer ones and start immediately."
        ),
        "why_worst_rt": (
            "Long processes in SRTF may be repeatedly preempted, delaying their "
            "first meaningful execution."
        ),
    },
}


def _find_best_worst(comparison_results, metric_key, lower_is_better=True):
    """Find the best and worst algorithm for a given metric."""
    items = list(comparison_results.items())
    if lower_is_better:
        best = min(items, key=lambda x: x[1][metric_key])
        worst = max(items, key=lambda x: x[1][metric_key])
    else:
        best = max(items, key=lambda x: x[1][metric_key])
        worst = min(items, key=lambda x: x[1][metric_key])
    return best, worst


def generate_analysis(comparison_results, scenario_name):
    """
    Generate a comprehensive textual analysis explaining WHY each
    algorithm performed the way it did for the given scenario.
    Returns a list of analysis strings.
    """
    analysis_lines = []
    analysis_lines.append(f"\n{'=' * 70}")
    analysis_lines.append(f"RESULT ANALYSIS -- Scenario: {scenario_name}")
    analysis_lines.append(f"{'=' * 70}")

    # ── Waiting Time Analysis ──
    best_wt, worst_wt = _find_best_worst(comparison_results, "avg_waiting_time")
    analysis_lines.append(f"\n-- Average Waiting Time --")
    analysis_lines.append(f"  BEST:  {best_wt[0]} ({best_wt[1]['avg_waiting_time']:.2f} t.u.)")
    analysis_lines.append(f"  WORST: {worst_wt[0]} ({worst_wt[1]['avg_waiting_time']:.2f} t.u.)")
    if best_wt[0] in ALGORITHM_TRAITS:
        analysis_lines.append(f"  WHY:   {ALGORITHM_TRAITS[best_wt[0]]['why_best_wt']}")
    if worst_wt[0] in ALGORITHM_TRAITS:
        analysis_lines.append(f"  WHY WORST: {ALGORITHM_TRAITS[worst_wt[0]]['why_worst_wt']}")

    # ── Turnaround Time Analysis ──
    best_tat, worst_tat = _find_best_worst(comparison_results, "avg_turnaround_time")
    analysis_lines.append(f"\n-- Average Turnaround Time --")
    analysis_lines.append(f"  BEST:  {best_tat[0]} ({best_tat[1]['avg_turnaround_time']:.2f} t.u.)")
    analysis_lines.append(f"  WORST: {worst_tat[0]} ({worst_tat[1]['avg_turnaround_time']:.2f} t.u.)")
    # TAT = WT + BT, so the explanation follows from WT
    analysis_lines.append(
        f"  NOTE:  Turnaround Time = Waiting Time + Burst Time. Since burst times "
        f"are constant across algorithms, TAT ranking mirrors WT ranking."
    )

    # ── Response Time Analysis ──
    best_rt, worst_rt = _find_best_worst(comparison_results, "avg_response_time")
    analysis_lines.append(f"\n-- Average Response Time --")
    analysis_lines.append(f"  BEST:  {best_rt[0]} ({best_rt[1]['avg_response_time']:.2f} t.u.)")
    analysis_lines.append(f"  WORST: {worst_rt[0]} ({worst_rt[1]['avg_response_time']:.2f} t.u.)")
    if best_rt[0] in ALGORITHM_TRAITS:
        analysis_lines.append(f"  WHY:   {ALGORITHM_TRAITS[best_rt[0]]['why_best_rt']}")
    if worst_rt[0] in ALGORITHM_TRAITS:
        analysis_lines.append(f"  WHY WORST: {ALGORITHM_TRAITS[worst_rt[0]]['why_worst_rt']}")

    # ── Throughput Discussion ──
    best_tp, worst_tp = _find_best_worst(comparison_results, "throughput", lower_is_better=False)
    analysis_lines.append(f"\n-- Throughput --")
    analysis_lines.append(f"  BEST:  {best_tp[0]} ({best_tp[1]['throughput']:.4f} proc/t.u.)")
    analysis_lines.append(f"  WORST: {worst_tp[0]} ({worst_tp[1]['throughput']:.4f} proc/t.u.)")

    # Check if throughput is the same across all algorithms
    tp_values = [v["throughput"] for v in comparison_results.values()]
    tp_range = max(tp_values) - min(tp_values)
    if tp_range < 0.001:
        analysis_lines.append(
            "  NOTE:  Throughput is effectively identical across all algorithms for this "
            "scenario. This is expected: for a fixed set of n processes with no idle "
            "gaps, the total observation window Delta = max(c_i) - min(a_i) is the same "
            "regardless of scheduling order. Throughput differences emerge only when "
            "algorithms introduce idle CPU time (e.g., due to late arrivals) or in "
            "continuous-arrival / open-system workloads."
        )
    else:
        analysis_lines.append(
            "  NOTE:  Throughput differs because some algorithms introduce CPU idle "
            "periods (gaps where no process is ready). Algorithms that minimize idle "
            "time achieve higher throughput."
        )

    # ── Scenario-Specific Observations ──
    analysis_lines.append(f"\n-- Scenario-Specific Observations --")
    scenario_lower = scenario_name.lower()
    if "convoy" in scenario_lower:
        analysis_lines.append(
            "  This scenario demonstrates the CONVOY EFFECT: a long CPU-bound process "
            "(P1 with burst=20) arrives first and blocks all subsequent short processes "
            "in FCFS. Non-preemptive algorithms suffer disproportionately. Preemptive "
            "algorithms (RR, SRTF) mitigate this by time-slicing or preempting."
        )
    elif "rr" in scenario_lower or "round" in scenario_lower:
        analysis_lines.append(
            "  This scenario is designed to favor Round Robin: all processes arrive at "
            "t=0, so RR's time-slicing ensures every process gets CPU access quickly. "
            "Response time is minimized because no process waits more than (n-1)*q "
            "time units before first execution."
        )
    elif "priority" in scenario_lower:
        analysis_lines.append(
            "  This scenario tests priority-based scheduling with diverse priority values. "
            "Priority Scheduling should excel when high-priority processes need fast service. "
            "However, low-priority processes risk starvation -- they may wait indefinitely "
            "if higher-priority processes keep arriving."
        )
    elif "srtf" in scenario_lower:
        analysis_lines.append(
            "  This scenario features staggered arrivals optimized to trigger preemptions. "
            "SRTF should achieve the lowest waiting/turnaround times by preempting long "
            "processes whenever a shorter one arrives."
        )
    elif "presentation" in scenario_lower:
        analysis_lines.append(
            "  This is a comprehensive mixed-workload stress test with varied burst times, "
            "priorities, and staggered arrivals. It tests all algorithms under realistic "
            "conditions where no single algorithm is inherently favored."
        )
    elif "live" in scenario_lower:
        analysis_lines.append(
            "  This scenario uses real process data extracted from the operating system. "
            "Burst times are estimated from CPU usage snapshots. Results should be "
            "interpreted with the understanding that real-world process behavior is "
            "non-deterministic and varies between executions."
        )
    else:
        analysis_lines.append(
            "  This is a baseline scenario with moderate parameters. Results provide "
            "a general comparison without extreme conditions."
        )

    analysis_lines.append(f"\n{'=' * 70}")

    # Print to console
    full_text = "\n".join(analysis_lines)
    print(full_text)

    return analysis_lines


def create_analysis_figure(comparison_results, scenario_name):
    """
    Create a matplotlib figure with the analysis text for the report.
    """
    analysis_lines = []

    # Build condensed analysis
    best_wt, worst_wt = _find_best_worst(comparison_results, "avg_waiting_time")
    best_tat, worst_tat = _find_best_worst(comparison_results, "avg_turnaround_time")
    best_rt, worst_rt = _find_best_worst(comparison_results, "avg_response_time")
    best_tp, _ = _find_best_worst(comparison_results, "throughput", lower_is_better=False)

    fig, ax = plt.subplots(figsize=(15, 12))
    ax.axis("off")

    ax.text(
        0.5, 0.98,
        f"Result Analysis & Motivation — {scenario_name}",
        transform=ax.transAxes,
        fontsize=16, fontweight="bold", ha="center", va="top",
        color="#1a1a2e"
    )

    y = 0.92

    # ── Metric Summary Table ──
    summary_data = [
        ["Metric", "Best Algorithm", "Value", "Worst Algorithm", "Value"],
        ["Avg Waiting Time", best_wt[0], f"{best_wt[1]['avg_waiting_time']:.2f} t.u.",
         worst_wt[0], f"{worst_wt[1]['avg_waiting_time']:.2f} t.u."],
        ["Avg Turnaround Time", best_tat[0], f"{best_tat[1]['avg_turnaround_time']:.2f} t.u.",
         worst_tat[0], f"{worst_tat[1]['avg_turnaround_time']:.2f} t.u."],
        ["Avg Response Time", best_rt[0], f"{best_rt[1]['avg_response_time']:.2f} t.u.",
         worst_rt[0], f"{worst_rt[1]['avg_response_time']:.2f} t.u."],
        ["Throughput", best_tp[0], f"{best_tp[1]['throughput']:.4f} proc/t.u.",
         "", ""],
    ]

    table = ax.table(
        cellText=summary_data[1:],
        colLabels=summary_data[0],
        cellLoc="center",
        loc="upper center",
        bbox=[0.05, 0.68, 0.90, 0.22]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#333333")
        cell.set_linewidth(0.8)
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#2c3e50")
        elif col == 1:  # Best algorithm column
            cell.set_facecolor("#d4edda")
        elif col == 3:  # Worst algorithm column
            cell.set_facecolor("#f8d7da")
        else:
            cell.set_facecolor("#f8f9fa")

    # ── WHY explanations ──
    y = 0.64
    explanations = [
        ("Why is {best} the best for Waiting Time?".format(best=best_wt[0]),
         ALGORITHM_TRAITS.get(best_wt[0], {}).get("why_best_wt", "N/A")),
        ("Why is {best} the best for Response Time?".format(best=best_rt[0]),
         ALGORITHM_TRAITS.get(best_rt[0], {}).get("why_best_rt", "N/A")),
    ]

    for question, answer in explanations:
        ax.text(0.05, y, question, transform=ax.transAxes,
                fontsize=11, fontweight="bold", color="#2c3e50", va="top")
        y -= 0.04
        wrapped = textwrap.fill(answer, width=110)
        ax.text(0.07, y, wrapped, transform=ax.transAxes,
                fontsize=9.5, va="top", color="#333333",
                bbox=dict(boxstyle="round,pad=0.4", edgecolor="#bdc3c7", facecolor="#f8f9fa"))
        y -= 0.04 * (wrapped.count("\n") + 2)

    # ── Throughput Discussion ──
    tp_values = [v["throughput"] for v in comparison_results.values()]
    tp_range = max(tp_values) - min(tp_values)

    ax.text(0.05, y, "Throughput Discussion:", transform=ax.transAxes,
            fontsize=11, fontweight="bold", color="#2c3e50", va="top")
    y -= 0.04

    if tp_range < 0.001:
        tp_text = (
            "Throughput is effectively identical across all algorithms (approx. {:.4f} proc/t.u.). "
            "This is expected for a fixed set of n processes: the observation window "
            "Delta = max(c_i) - min(a_i) is determined by the workload, not the scheduling order. "
            "Throughput differentiation requires continuous process arrivals or multi-queue scenarios."
        ).format(tp_values[0])
    else:
        tp_text = (
            "Throughput varies across algorithms because some introduce CPU idle periods. "
            "{best} achieves the highest throughput ({val:.4f} proc/t.u.) by minimizing "
            "idle gaps in the schedule."
        ).format(best=best_tp[0], val=best_tp[1]['throughput'])

    wrapped_tp = textwrap.fill(tp_text, width=110)
    ax.text(0.07, y, wrapped_tp, transform=ax.transAxes,
            fontsize=9.5, va="top", color="#333333",
            bbox=dict(boxstyle="round,pad=0.4", edgecolor="#bdc3c7", facecolor="#fff8e1"))

    plt.tight_layout()
    return fig
