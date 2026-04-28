"""
formulas.py — Formal Metric Definitions and Mathematical Formulas

This module provides the mathematical foundation for all performance
metrics used in the CPU scheduling simulation. Formulas are presented
both as structured console output and as a LaTeX-rendered matplotlib
figure suitable for inclusion in academic reports.

"""

import matplotlib.pyplot as plt
import matplotlib


def print_metric_definitions():
    """Print formal metric definitions to the console."""
    print("\n" + "=" * 70)
    print("FORMAL METRIC DEFINITIONS")
    print("=" * 70)
    print("""
Let  P = {p_1, p_2, ..., p_n}  be the set of n processes submitted to the scheduler.

For each process p_i the following attributes are defined:

  a_i  = Arrival Time   : the time at which p_i enters the ready queue
  b_i  = Burst Time     : the total CPU time required by p_i
  s_i  = Start Time     : the time at which p_i first receives the CPU
  c_i  = Completion Time: the time at which p_i finishes execution

---------------------------------------------------------------------
METRIC FORMULAS (per-process)
---------------------------------------------------------------------

  Turnaround Time :   TAT_i  =  c_i  -  a_i
  Waiting Time    :   WT_i   =  TAT_i -  b_i   =  c_i - a_i - b_i
  Response Time   :   RT_i   =  s_i  -  a_i

---------------------------------------------------------------------
AGGREGATE FORMULAS (across all n processes)
---------------------------------------------------------------------

  Average Waiting Time      :  Avg(WT)   =  (1/n)  *  SUM(WT_i)
  Average Turnaround Time   :  Avg(TAT)  =  (1/n)  *  SUM(TAT_i)
  Average Response Time     :  Avg(RT)   =  (1/n)  *  SUM(RT_i)

  Throughput                :  lambda  =  n / ( max(c_i) - min(a_i) )
     where the denominator is the total observation window Delta.

---------------------------------------------------------------------
OBSERVATION WINDOW (Delta)
---------------------------------------------------------------------

  Delta  =  max(c_i) - min(a_i)

  The observation window is the elapsed time from the arrival of the
  first process until the completion of the last process. All metrics
  are computed in steady state within this window.

---------------------------------------------------------------------
FCFS -- Waiting Time Recurrence
---------------------------------------------------------------------

  For FCFS with processes sorted by arrival time:
    WT_1  =  0                           (first process never waits)
    WT_i  =  (a_{i-1} + b_{i-1} + WT_{i-1}) - a_i    for i > 1

  Average Waiting Time  =  SUM(WT_i) / n
""")
    print("=" * 70)


def create_formulas_figure():
    """
    Create a matplotlib figure that renders the metric formulas
    using LaTeX-style typesetting for inclusion in the report.
    """
    fig, ax = plt.subplots(figsize=(14, 12))
    ax.axis("off")

    # Title
    ax.text(
        0.5, 0.98,
        "Formal Metric Definitions & Mathematical Formulas",
        transform=ax.transAxes,
        fontsize=18, fontweight="bold", ha="center", va="top",
        color="#1a1a2e"
    )

    # Use mathtext (matplotlib built-in) instead of requiring full LaTeX
    matplotlib.rcParams['mathtext.fontset'] = 'cm'

    sections = [
        {
            "title": "1. Per-Process Variables",
            "content": (
                r"Let  $P = \{p_1, p_2, \ldots, p_n\}$  be the set of $n$ processes."
                "\n"
                r"For each process $p_i$:  $a_i$ = Arrival Time,  $b_i$ = Burst Time,  $s_i$ = Start Time,  $c_i$ = Completion Time"
            )
        },
        {
            "title": "2. Per-Process Metrics",
            "content": (
                r"Turnaround Time:      $TAT_i = c_i - a_i$"
                "\n"
                r"Waiting Time:            $WT_i = TAT_i - b_i = c_i - a_i - b_i$"
                "\n"
                r"Response Time:          $RT_i = s_i - a_i$"
            )
        },
        {
            "title": "3. Aggregate Metrics",
            "content": (
                r"Average Waiting Time:           $\overline{WT} = \frac{1}{n} \sum_{i=1}^{n} WT_i$"
                "\n"
                r"Average Turnaround Time:     $\overline{TAT} = \frac{1}{n} \sum_{i=1}^{n} TAT_i$"
                "\n"
                r"Average Response Time:         $\overline{RT} = \frac{1}{n} \sum_{i=1}^{n} RT_i$"
            )
        },
        {
            "title": "4. Throughput & Observation Window",
            "content": (
                r"Observation Window:   $\Delta = \max(c_i) - \min(a_i)$"
                "\n"
                r"Throughput:                  $\lambda = \frac{n}{\Delta}$   (processes completed per time unit)"
            )
        },
        {
            "title": "5. FCFS Waiting Time Recurrence",
            "content": (
                r"$WT_1 = 0$   (first process never waits)"
                "\n"
                r"$WT_i = (a_{i-1} + b_{i-1} + WT_{i-1}) - a_i$   for $i > 1$"
                "\n"
                r"Average Waiting Time  $= \frac{\sum_{i=1}^{n} WT_i}{n}$"
            )
        },
    ]

    y_pos = 0.90
    for section in sections:
        # Section title
        ax.text(
            0.05, y_pos,
            section["title"],
            transform=ax.transAxes,
            fontsize=13, fontweight="bold", color="#2c3e50",
            va="top"
        )
        y_pos -= 0.03

        # Section content — render each line separately for math support
        lines = section["content"].split("\n")
        for line in lines:
            ax.text(
                0.08, y_pos,
                line.strip(),
                transform=ax.transAxes,
                fontsize=11, va="top", color="#333333"
            )
            y_pos -= 0.03

        y_pos -= 0.02  # spacing between sections

    # References box at the bottom
    ref_text = (
        "References:\n"
        "  [1] Silberschatz, Galvin, Gagne — Operating System Concepts (10th Ed.), Ch. 5\n"
        "  [2] Neetu Goel, Dr. R.B. Garg “A Comparative Study of CPU Scheduling Algorithms.” TEERTHANKER MAHAVEER UNIVERSITY, Delhi School of Professional Studies & Research.\n"
        "  [3] M. Rajasekhar Reddy, V.V.D.S.S. Ganesh, S. Lakshmi, Yerramreddy Sireesha “Comparative Analysis of CPU Scheduling Algorithms and Their Optimal Solutions."
    )
    ax.text(
        0.05, 0.04,
        ref_text,
        transform=ax.transAxes,
        fontsize=9, va="bottom", color="#555555",
        family="monospace",
        bbox=dict(boxstyle="round,pad=0.5", edgecolor="#cccccc", facecolor="#f9f9f9")
    )

    plt.tight_layout()
    return fig
