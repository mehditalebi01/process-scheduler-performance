"""
context.py — Test Bed Context, Limitations, and Observation Window

This module defines and documents the simulation environment, including
the assumptions, constraints, and limitations of the test bed. This
information is critical for interpreting the results correctly and
understanding the scope of the evaluation.

References:
    [1] Silberschatz, Galvin, Gagne — "Operating System Concepts" (10th Ed.), Ch. 5
    
"""

import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────────────
# Test Bed Configuration
# ─────────────────────────────────────────────────────────────────────

TIME_UNIT = "t.u."  # Abstract time units
TIME_UNIT_FULL = "Abstract Time Units (t.u.)"

TESTBED_CONTEXT = {
    "environment": "Single-CPU, single-core simulation (no multiprocessor scheduling)",
    "time_unit": TIME_UNIT_FULL,
    "time_unit_note": (
        "Time is measured in abstract time units (t.u.). In real operating systems, "
        "1 t.u. may correspond to milliseconds, microseconds, or CPU clock cycles "
        "depending on the hardware and workload characteristics. For reference, "
        "typical OS time slices range from 10-100 ms (Tanenbaum, 2014)."
    ),
    "observation_window": (
        "Steady-state observation from Delta = max(c_i) - min(a_i), "
        "i.e., from the arrival of the first process to the completion of the last."
    ),
    "num_processes": "4-6 per scenario (Scenarios 1-6), variable for live scenario",
    "quantum_rr": 2,
    "priority_convention": "Lower integer = higher priority (1 = highest)",
    "scheduling_model": "Non-preemptive (FCFS, SJF, Priority) and Preemptive (RR, SRTF)",
}

TESTBED_ASSUMPTIONS = [
    "All processes are CPU-bound (no I/O bursts modeled)",
    "Context-switch overhead is assumed to be zero (instantaneous preemption)",
    "Processes are independent -- no inter-process communication or synchronization",
    "Ready queue management follows FIFO ordering for tie-breaking",
    "Burst times are known a priori (deterministic workloads)",
    "Single-processor environment -- no parallel execution",
]

TESTBED_LIMITATIONS = [
    "Small number of processes (n <= 6) -- results may not generalize to high-load scenarios",
    "Integer-only burst and arrival times -- real systems exhibit continuous distributions",
    "No I/O operations -- does not capture the behavior of I/O-bound or mixed workloads",
    "No context-switch overhead -- preemptive algorithms (RR, SRTF) appear more efficient than in practice",
    "No aging mechanism -- starvation in Priority and SJF is not mitigated",
    "Deterministic workloads -- does not model stochastic process arrivals (e.g., Poisson distribution)",
]


def print_testbed_context():
    """Print the test bed context and limitations to the console."""
    print("\n" + "=" * 70)
    print("SIMULATION TEST BED CONTEXT")
    print("=" * 70)

    print("\nEnvironment Configuration:")
    for key, value in TESTBED_CONTEXT.items():
        label = key.replace("_", " ").title()
        print(f"  {label:30s}: {value}")

    print("\nAssumptions:")
    for i, assumption in enumerate(TESTBED_ASSUMPTIONS, 1):
        print(f"  {i}. {assumption}")

    print("\nLimitations:")
    for i, limitation in enumerate(TESTBED_LIMITATIONS, 1):
        print(f"  {i}. {limitation}")

    print("=" * 70)


def create_context_figure():
    """
    Create a matplotlib figure summarizing the test bed context,
    assumptions, and limitations for the report.
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 14),
                             gridspec_kw={'height_ratios': [1.2, 1, 1.2]})

    for ax in axes:
        ax.axis("off")

    fig.suptitle(
        "Simulation Test Bed — Context & Limitations",
        fontsize=18, fontweight="bold", color="#1a1a2e", y=0.98
    )

    # ── Panel 1: Environment Configuration ──
    config_lines = []
    for key, value in TESTBED_CONTEXT.items():
        label = key.replace("_", " ").title()
        # Truncate long values for display
        val_str = str(value)
        if len(val_str) > 90:
            val_str = val_str[:87] + "..."
        config_lines.append(f"{label:32s}  {val_str}")

    config_text = "\n".join(config_lines)
    axes[0].text(
        0.03, 0.95,
        "Environment Configuration",
        transform=axes[0].transAxes,
        fontsize=14, fontweight="bold", color="#2c3e50", va="top"
    )
    axes[0].text(
        0.03, 0.82,
        config_text,
        transform=axes[0].transAxes,
        fontsize=9, va="top", family="monospace", color="#333333",
        bbox=dict(boxstyle="round,pad=0.6", edgecolor="#bdc3c7", facecolor="#f8f9fa")
    )

    # ── Panel 2: Assumptions ──
    axes[1].text(
        0.03, 0.95,
        "Assumptions",
        transform=axes[1].transAxes,
        fontsize=14, fontweight="bold", color="#2c3e50", va="top"
    )
    assumptions_text = "\n".join(
        f"  {i}. {a}" for i, a in enumerate(TESTBED_ASSUMPTIONS, 1)
    )
    axes[1].text(
        0.03, 0.80,
        assumptions_text,
        transform=axes[1].transAxes,
        fontsize=10, va="top", color="#333333",
        bbox=dict(boxstyle="round,pad=0.6", edgecolor="#bdc3c7", facecolor="#f8f9fa")
    )

    # ── Panel 3: Limitations ──
    axes[2].text(
        0.03, 0.95,
        "Limitations",
        transform=axes[2].transAxes,
        fontsize=14, fontweight="bold", color="#c0392b", va="top"
    )
    limitations_text = "\n".join(
        f"  {i}. {l}" for i, l in enumerate(TESTBED_LIMITATIONS, 1)
    )
    axes[2].text(
        0.03, 0.80,
        limitations_text,
        transform=axes[2].transAxes,
        fontsize=10, va="top", color="#333333",
        bbox=dict(boxstyle="round,pad=0.6", edgecolor="#e74c3c", facecolor="#fdf2f2")
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig
