"""
sample_data.py — Workload Test Scenarios

This module defines all process sets used in the simulation, including
six carefully designed synthetic scenarios and one live-system scenario
that reads real process data from the operating system.

Each scenario returns a list of Process objects with defined PID,
arrival_time, burst_time, and priority attributes.
"""

from process import Process


# ═══════════════════════════════════════════════════════════════════════
# Scenario 1: Basic — Baseline test
# ═══════════════════════════════════════════════════════════════════════

def scenario_basic():
    """
    Scenario 1: Basic
    A baseline case with moderate arrival times and burst durations.
    Tests general algorithm functionality without extreme conditions.
    """
    return [
        Process("P1", arrival_time=0, burst_time=5, priority=2),
        Process("P2", arrival_time=1, burst_time=3, priority=1),
        Process("P3", arrival_time=2, burst_time=8, priority=3),
        Process("P4", arrival_time=3, burst_time=6, priority=2),
    ]


# ═══════════════════════════════════════════════════════════════════════
# Scenario 2: Convoy Effect — Demonstrates FCFS weakness
# ═══════════════════════════════════════════════════════════════════════

def scenario_convoy_effect():
    """
    Scenario 2: Convoy Effect
    A massive CPU-bound process (P1, burst=20) arrives first, followed
    by several very short processes. Explicitly demonstrates the convoy
    effect in FCFS where short processes are stuck behind long ones.
    """
    return [
        Process("P1", arrival_time=0, burst_time=20, priority=3),
        Process("P2", arrival_time=1, burst_time=2, priority=1),
        Process("P3", arrival_time=2, burst_time=2, priority=1),
        Process("P4", arrival_time=3, burst_time=2, priority=2),
        Process("P5", arrival_time=4, burst_time=2, priority=2),
    ]


# ═══════════════════════════════════════════════════════════════════════
# Scenario 3: RR Friendly — Favors time-sharing
# ═══════════════════════════════════════════════════════════════════════

def scenario_rr_friendly():
    """
    Scenario 3: RR Friendly
    Simultaneous arrivals (all at t=0) with varying burst times.
    Designed to favor Round Robin: time-slicing ensures every process
    gets CPU access quickly, minimizing response time.
    """
    return [
        Process("P1", arrival_time=0, burst_time=9, priority=3),
        Process("P2", arrival_time=0, burst_time=5, priority=1),
        Process("P3", arrival_time=0, burst_time=7, priority=2),
        Process("P4", arrival_time=0, burst_time=3, priority=1),
        Process("P5", arrival_time=0, burst_time=1, priority=2),
    ]


# ═══════════════════════════════════════════════════════════════════════
# Scenario 4: Priority Case — Tests priority-based scheduling
# ═══════════════════════════════════════════════════════════════════════

def scenario_priority_case():
    """
    Scenario 4: Priority Case
    Diverse priority values to evaluate priority inversion risks and
    strict priority-based scheduling mechanics.
    """
    return [
        Process("P1", arrival_time=0, burst_time=8, priority=3),
        Process("P2", arrival_time=1, burst_time=4, priority=1),
        Process("P3", arrival_time=2, burst_time=9, priority=5),
        Process("P4", arrival_time=3, burst_time=5, priority=2),
        Process("P5", arrival_time=4, burst_time=2, priority=4),
    ]


# ═══════════════════════════════════════════════════════════════════════
# Scenario 5: SRTF Case — Optimized for preemption
# ═══════════════════════════════════════════════════════════════════════

def scenario_srtf_case():
    """
    Scenario 5: SRTF Case
    Staggered, continuous arrivals specifically optimized to trigger
    preemptions and showcase the efficiency of shortest-remaining-time.
    """
    return [
        Process("P1", arrival_time=0, burst_time=12, priority=3),
        Process("P2", arrival_time=2, burst_time=2, priority=1),
        Process("P3", arrival_time=4, burst_time=1, priority=2),
        Process("P4", arrival_time=6, burst_time=3, priority=2),
        Process("P5", arrival_time=8, burst_time=2, priority=1),
    ]


# ═══════════════════════════════════════════════════════════════════════
# Scenario 6: Presentation — Complex mixed workload
# ═══════════════════════════════════════════════════════════════════════

def scenario_presentation():
    """
    Scenario 6: Presentation
    A complex, mixed workload with varied burst times, priorities, and
    staggered arrivals. Serves as a comprehensive stress test.
    """
    return [
        Process("P1", arrival_time=0, burst_time=15, priority=4),
        Process("P2", arrival_time=1, burst_time=3, priority=1),
        Process("P3", arrival_time=2, burst_time=6, priority=3),
        Process("P4", arrival_time=3, burst_time=1, priority=2),
        Process("P5", arrival_time=4, burst_time=8, priority=5),
        Process("P6", arrival_time=5, burst_time=4, priority=2),
    ]


# ═══════════════════════════════════════════════════════════════════════
# Scenario 7: Live System — Real process data from the OS
# ═══════════════════════════════════════════════════════════════════════

def scenario_live_system():
    """
    Scenario 7: Live System
    Reads real running processes from the operating system using psutil.
    Selects processes with measurable CPU activity and maps their real
    PIDs and estimated burst times into the simulation.

    Burst times are estimated by scaling CPU usage percentage into
    abstract time units. Arrival times are staggered based on process
    creation order.

    Falls back to a predefined set if psutil is not available.
    """
    try:
        import psutil

        # Get a snapshot of running processes with CPU info
        # We need two calls to get meaningful cpu_percent values
        all_procs = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'status']):
            try:
                info = proc.info
                if info['status'] == psutil.STATUS_RUNNING or info['cpu_percent'] is not None:
                    all_procs.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Wait briefly and re-sample for accurate CPU percentages
        import time
        time.sleep(0.5)

        sampled = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                info = proc.info
                if info['cpu_percent'] and info['cpu_percent'] > 0:
                    sampled.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort by CPU usage (descending) and take top 6-8 processes
        sampled.sort(key=lambda x: x['cpu_percent'], reverse=True)
        selected = sampled[:8] if len(sampled) >= 8 else sampled[:max(len(sampled), 4)]

        if len(selected) < 3:
            print("  [INFO] Not enough active processes found, using fallback data.")
            return _live_fallback()

        processes = []
        for i, proc_info in enumerate(selected):
            pid_str = str(proc_info['pid'])
            # Scale CPU percentage to burst time (1-20 range)
            burst = max(1, min(20, int(proc_info['cpu_percent'] / 5) + 1))
            # Stagger arrival times
            arrival = i
            # Assign priority based on CPU usage (higher usage = higher priority)
            priority = max(1, min(5, 6 - int(proc_info['cpu_percent'] / 20) - 1))

            name_label = proc_info.get('name', pid_str)
            if name_label and len(name_label) > 12:
                name_label = name_label[:12]

            processes.append(
                Process(f"{name_label}({pid_str})", arrival_time=arrival,
                        burst_time=burst, priority=priority)
            )

        print(f"  [LIVE] Captured {len(processes)} real processes from the system:")
        for p in processes:
            print(f"    PID={p.pid}, Arrival={p.arrival_time}, "
                  f"Burst={p.burst_time}, Priority={p.priority}")

        return processes

    except ImportError:
        print("  [WARNING] psutil not installed. Using fallback data.")
        print("  Install with: pip install psutil")
        return _live_fallback()
    except Exception as e:
        print(f"  [ERROR] Failed to read live processes: {e}")
        print("  Using fallback data.")
        return _live_fallback()


def _live_fallback():
    """
    Fallback process set simulating realistic process characteristics
    when psutil is not available or live capture fails.
    Uses realistic PID numbers and process-like names.
    """
    return [
        Process("chrome(4832)", arrival_time=0, burst_time=8, priority=3),
        Process("python(2156)", arrival_time=1, burst_time=4, priority=2),
        Process("vscode(3088)", arrival_time=2, burst_time=6, priority=3),
        Process("system(4)", arrival_time=0, burst_time=2, priority=1),
        Process("explorer(1924)", arrival_time=3, burst_time=3, priority=2),
        Process("svchost(876)", arrival_time=1, burst_time=5, priority=1),
    ]
