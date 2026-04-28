"""
schedulers.py — CPU Scheduling Algorithm Implementations

This module implements five fundamental CPU scheduling algorithms with
full pseudocode documentation, formal descriptions, and academic references.

Each algorithm function returns:
    schedule  — list of (pid, start_time, end_time) tuples for Gantt chart rendering
    completed — list of dicts with per-process metrics

"""

import matplotlib.pyplot as plt


# ═══════════════════════════════════════════════════════════════════════
# Pseudocode text for each algorithm (used by create_pseudocode_figure)
# ═══════════════════════════════════════════════════════════════════════

PSEUDOCODE = {
    "FCFS": (
        "PROCEDURE FCFS(P):\n"
        "    SORT P by arrival_time (ascending)\n"
        "    current_time ← 0\n"
        "    FOR EACH process p IN P:\n"
        "        IF current_time < p.arrival_time:\n"
        "            current_time ← p.arrival_time   // CPU idle\n"
        "        p.start_time ← current_time\n"
        "        p.completion_time ← current_time + p.burst_time\n"
        "        p.TAT ← p.completion_time − p.arrival_time\n"
        "        p.WT  ← p.TAT − p.burst_time\n"
        "        p.RT  ← p.start_time − p.arrival_time\n"
        "        current_time ← p.completion_time\n"
        "    RETURN schedule, completed\n"
        "\n"
        "Complexity: O(n log n) — dominated by initial sort\n"
        "Type: Non-preemptive"
    ),
    "SJF": (
        "PROCEDURE SJF(P):\n"
        "    SORT P by arrival_time (ascending)\n"
        "    current_time ← 0\n"
        "    completed_count ← 0\n"
        "    WHILE completed_count < n:\n"
        "        ready ← {p ∈ P : p.arrived ≤ current_time AND NOT visited}\n"
        "        IF ready = ∅:\n"
        "            current_time ← current_time + 1\n"
        "            CONTINUE\n"
        "        p* ← argmin(ready, key=burst_time)  // select shortest job\n"
        "        p*.start_time ← current_time\n"
        "        p*.completion_time ← current_time + p*.burst_time\n"
        "        p*.TAT ← p*.completion_time − p*.arrival_time\n"
        "        p*.WT  ← p*.TAT − p*.burst_time\n"
        "        p*.RT  ← p*.start_time − p*.arrival_time\n"
        "        current_time ← p*.completion_time\n"
        "        completed_count ← completed_count + 1\n"
        "    RETURN schedule, completed\n"
        "\n"
        "Complexity: O(n²) — selection from ready queue at each step\n"
        "Type: Non-preemptive\n"
        "Optimality: Minimizes avg WT among non-preemptive algorithms [1]"
    ),
    "RR": (
        "PROCEDURE RoundRobin(P, quantum=q):\n"
        "    SORT P by arrival_time (ascending)\n"
        "    current_time ← 0\n"
        "    ready_queue ← empty FIFO queue\n"
        "    WHILE NOT all processes completed:\n"
        "        ENQUEUE newly arrived processes to ready_queue\n"
        "        IF ready_queue = ∅:\n"
        "            current_time ← current_time + 1\n"
        "            CONTINUE\n"
        "        p ← DEQUEUE(ready_queue)\n"
        "        IF p.start_time = NULL:\n"
        "            p.start_time ← current_time\n"
        "        exec_time ← min(q, p.remaining_time)\n"
        "        current_time ← current_time + exec_time\n"
        "        p.remaining_time ← p.remaining_time − exec_time\n"
        "        ENQUEUE newly arrived processes\n"
        "        IF p.remaining_time > 0:\n"
        "            ENQUEUE p to back of ready_queue\n"
        "        ELSE:\n"
        "            p.completion_time ← current_time\n"
        "            COMPUTE TAT, WT, RT\n"
        "    RETURN schedule, completed\n"
        "\n"
        "Complexity: O(n × total_burst / q)\n"
        "Type: Preemptive (time-sharing)\n"
        "Note: q=2 in this simulation"
    ),
    "Priority": (
        "PROCEDURE PriorityScheduling(P):\n"
        "    SORT P by arrival_time (ascending)\n"
        "    current_time ← 0\n"
        "    completed_count ← 0\n"
        "    WHILE completed_count < n:\n"
        "        ready ← {p ∈ P : p.arrived ≤ current_time AND NOT visited}\n"
        "        IF ready = ∅:\n"
        "            current_time ← current_time + 1\n"
        "            CONTINUE\n"
        "        p* ← argmin(ready, key=priority)  // lowest value = highest priority\n"
        "        // Tie-breaking: FCFS (earliest arrival_time)\n"
        "        p*.start_time ← current_time\n"
        "        p*.completion_time ← current_time + p*.burst_time\n"
        "        p*.TAT ← p*.completion_time − p*.arrival_time\n"
        "        p*.WT  ← p*.TAT − p*.burst_time\n"
        "        p*.RT  ← p*.start_time − p*.arrival_time\n"
        "        current_time ← p*.completion_time\n"
        "        completed_count ← completed_count + 1\n"
        "    RETURN schedule, completed\n"
        "\n"
        "Complexity: O(n²)\n"
        "Type: Non-preemptive\n"
        "Convention: priority 1 = highest, 5 = lowest"
    ),
    "SRTF": (
        "PROCEDURE SRTF(P):\n"
        "    SORT P by arrival_time (ascending)\n"
        "    current_time ← 0\n"
        "    completed_count ← 0\n"
        "    WHILE completed_count < n:\n"
        "        ready ← {p ∈ P : p.arrived ≤ current_time AND p.remaining > 0}\n"
        "        IF ready = ∅:\n"
        "            current_time ← current_time + 1\n"
        "            CONTINUE\n"
        "        p* ← argmin(ready, key=remaining_time)\n"
        "        IF p*.start_time = NULL:\n"
        "            p*.start_time ← current_time\n"
        "        EXECUTE p* for 1 time unit\n"
        "        p*.remaining_time ← p*.remaining_time − 1\n"
        "        current_time ← current_time + 1\n"
        "        IF p*.remaining_time = 0:\n"
        "            p*.completion_time ← current_time\n"
        "            COMPUTE TAT, WT, RT\n"
        "            completed_count ← completed_count + 1\n"
        "    RETURN schedule, completed\n"
        "\n"
        "Complexity: O(n × total_burst)\n"
        "Type: Preemptive\n"
        "Optimality: Minimizes avg WT among ALL algorithms [1]"
    ),
}


def create_pseudocode_figure():
    """
    Create a matplotlib figure rendering the pseudocode for all five
    scheduling algorithms, suitable for inclusion in the report.
    """
    fig = plt.figure(figsize=(18, 11.5))
    
    # GridSpec for finer layout control
    gs = fig.add_gridspec(3, 2)
    
    ax_fcfs = fig.add_subplot(gs[0, 0])
    ax_sjf = fig.add_subplot(gs[0, 1])
    ax_rr = fig.add_subplot(gs[1, 0])
    ax_priority = fig.add_subplot(gs[1, 1])
    ax_srtf = fig.add_subplot(gs[2, :])  # Span both columns
    
    axes_list = [ax_fcfs, ax_sjf, ax_rr, ax_priority, ax_srtf]

    titles = [
        ("FCFS", "Algorithm 1: First-Come-First-Served (FCFS) -- Non-Preemptive"),
        ("SJF", "Algorithm 2: Shortest Job First (SJF) -- Non-Preemptive"),
        ("RR", "Algorithm 3: Round Robin (RR, q=2) -- Preemptive"),
        ("Priority", "Algorithm 4: Priority Scheduling -- Non-Preemptive"),
        ("SRTF", "Algorithm 5: Shortest Remaining Time First (SRTF) -- Preemptive"),
    ]

    for i, (key, title) in enumerate(titles):
        ax = axes_list[i]
        ax.axis("off")
        
        # Center the 5th algorithm horizontally, but keep text left-aligned
        if i == 4:
            ax.set_title(title, fontsize=11, fontweight="bold", color="#2c3e50", pad=5, loc="center")
            ax.text(
                0.33, 1.05,
                PSEUDOCODE[key],
                transform=ax.transAxes,
                fontsize=7.5, va="top", ha="left", family="monospace", color="#1a1a2e",
                bbox=dict(boxstyle="round,pad=0.6", edgecolor="#2c3e50", facecolor="#f0f4f8")
            )
        else:
            ax.set_title(title, fontsize=11, fontweight="bold", color="#2c3e50", pad=5, loc="left")
            ax.text(
                0.02, 0.95,
                PSEUDOCODE[key],
                transform=ax.transAxes,
                fontsize=7.5, va="top", ha="left", family="monospace", color="#1a1a2e",
                bbox=dict(boxstyle="round,pad=0.6", edgecolor="#2c3e50", facecolor="#f0f4f8")
            )

    fig.suptitle(
        "Scheduling Algorithms -- Pseudocode",
        fontsize=16, fontweight="bold", color="#1a1a2e", y=0.98
    )
    plt.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.02, hspace=0.8, wspace=0.05)
    return fig


# ═══════════════════════════════════════════════════════════════════════
# Algorithm Implementations
# ═══════════════════════════════════════════════════════════════════════


def fcfs(processes):
    """
    First-Come-First-Served (FCFS) Scheduling Algorithm.

    Description:
        A non-preemptive algorithm that schedules processes strictly in the
        order they arrive in the ready queue. Uses a FIFO queue structure.

    Algorithm:
        1. Sort all processes by arrival time (ascending).
        2. For each process in order:
           a. If CPU is idle (current_time < arrival), advance clock.
           b. Execute process to completion (non-preemptive).
           c. Compute: WT = TAT - burst_time, TAT = completion - arrival,
              RT = start - arrival.

    Formulas:
        WT₁ = 0
        WTᵢ = (aᵢ₋₁ + bᵢ₋₁ + WTᵢ₋₁) − aᵢ   for i > 1
        Avg WT = (1/n) × Σ WTᵢ

    Complexity: O(n log n)

    References:
        [1] Silberschatz et al., "Operating System Concepts", 10th Ed., Ch. 5.3.1
    """
    processes = sorted(processes, key=lambda p: p.arrival_time)

    current_time = 0
    schedule = []
    completed = []

    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        start_time = current_time
        end_time = start_time + process.burst_time

        completion_time = end_time
        turnaround_time = completion_time - process.arrival_time
        waiting_time = turnaround_time - process.burst_time
        response_time = start_time - process.arrival_time

        completed.append({
            "pid": process.pid,
            "arrival_time": process.arrival_time,
            "burst_time": process.burst_time,
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "response_time": response_time,
        })

        schedule.append((process.pid, start_time, end_time))
        current_time = end_time

    return schedule, completed



def sjf(processes):
    """
    Shortest Job First (SJF) Scheduling Algorithm.

    Description:
        A non-preemptive algorithm that selects the waiting process with
        the smallest burst (execution) time. Mathematically proven to
        provide the minimum average waiting time among non-preemptive
        scheduling algorithms.

    Algorithm:
        1. Sort processes by arrival time.
        2. At each scheduling decision:
           a. Build ready set: all arrived, unvisited processes.
           b. Select process with minimum burst_time (tie-break by arrival).
           c. Execute to completion.
           d. Compute metrics.

    Formulas:
        p* = argmin{bᵢ : pᵢ ∈ ReadyQueue}
        WTᵢ = cᵢ − aᵢ − bᵢ
        Avg WT = (1/n) × Σ WTᵢ   (minimized by SJF)

    Complexity: O(n²)

            job ahead of a longer one always reduces total waiting time.
    """
    processes = sorted(processes, key=lambda p: p.arrival_time)
    n = len(processes)

    current_time = 0
    completed_count = 0
    visited = [False] * n

    schedule = []
    completed = []

    while completed_count < n:
        ready_processes = []

        for i in range(n):
            if not visited[i] and processes[i].arrival_time <= current_time:
                ready_processes.append((i, processes[i]))

        if not ready_processes:
            current_time += 1
            continue

        selected_index, selected_process = min(
            ready_processes,
            key=lambda x: (x[1].burst_time, x[1].arrival_time)
        )

        start_time = current_time
        end_time = start_time + selected_process.burst_time

        completion_time = end_time
        turnaround_time = completion_time - selected_process.arrival_time
        waiting_time = turnaround_time - selected_process.burst_time
        response_time = start_time - selected_process.arrival_time

        completed.append({
            "pid": selected_process.pid,
            "arrival_time": selected_process.arrival_time,
            "burst_time": selected_process.burst_time,
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "response_time": response_time,
        })

        schedule.append((selected_process.pid, start_time, end_time))

        visited[selected_index] = True
        completed_count += 1
        current_time = end_time

    return schedule, completed



def round_robin(processes, quantum=2):
    """
    Round Robin (RR) Scheduling Algorithm.

    Description:
        A preemptive algorithm designed for time-sharing systems. Each
        process receives a fixed time quantum (q). If a process does not
        finish within its quantum, it is preempted and placed at the back
        of the ready queue.

    Algorithm:
        1. Sort processes by arrival time.
        2. Maintain a FIFO ready queue.
        3. At each step:
           a. Enqueue newly arrived processes.
           b. Dequeue front process.
           c. Execute for min(q, remaining_time).
           d. If remaining_time > 0: re-enqueue to back.
           e. If remaining_time = 0: mark completed, compute metrics.

    Formulas:
        exec_time = min(q, remaining_timeᵢ)
        Context switches ≤ Σ⌈bᵢ/q⌉
        RTᵢ = sᵢ − aᵢ   (bounded by (n−1) × q for simultaneous arrivals)

    Parameters:
        quantum (int): Time quantum per scheduling round. Default is 2.

    Complexity: O(n × Σbᵢ / q)

    """
    processes = sorted(processes, key=lambda p: p.arrival_time)

    n = len(processes)
    current_time = 0
    schedule = []
    completed = []

    process_data = []
    for p in processes:
        process_data.append({
            "pid": p.pid,
            "arrival_time": p.arrival_time,
            "burst_time": p.burst_time,
            "priority": p.priority,
            "remaining_time": p.burst_time,
            "start_time": None,
            "completion_time": 0,
        })

    ready_queue = []
    arrived_index = 0
    completed_count = 0

    while completed_count < n:
        while arrived_index < n and process_data[arrived_index]["arrival_time"] <= current_time:
            ready_queue.append(process_data[arrived_index])
            arrived_index += 1

        if not ready_queue:
            current_time += 1
            continue

        current_process = ready_queue.pop(0)

        if current_process["start_time"] is None:
            current_process["start_time"] = current_time

        execution_time = min(quantum, current_process["remaining_time"])
        start_time = current_time
        end_time = current_time + execution_time

        schedule.append((current_process["pid"], start_time, end_time))

        current_time = end_time
        current_process["remaining_time"] -= execution_time

        while arrived_index < n and process_data[arrived_index]["arrival_time"] <= current_time:
            ready_queue.append(process_data[arrived_index])
            arrived_index += 1

        if current_process["remaining_time"] > 0:
            ready_queue.append(current_process)
        else:
            current_process["completion_time"] = current_time
            turnaround_time = current_process["completion_time"] - current_process["arrival_time"]
            waiting_time = turnaround_time - current_process["burst_time"]
            response_time = current_process["start_time"] - current_process["arrival_time"]

            completed.append({
                "pid": current_process["pid"],
                "arrival_time": current_process["arrival_time"],
                "burst_time": current_process["burst_time"],
                "start_time": current_process["start_time"],
                "completion_time": current_process["completion_time"],
                "waiting_time": waiting_time,
                "turnaround_time": turnaround_time,
                "response_time": response_time,
            })

            completed_count += 1

    return schedule, completed




def priority_scheduling(processes):
    """
    Priority Scheduling Algorithm.

    Description:
        A non-preemptive algorithm where the CPU is allocated to the
        process with the highest priority (lowest integer value). In the
        event of a tie, FCFS ordering is used as a tie-breaker.

    Algorithm:
        1. Sort processes by arrival time.
        2. At each scheduling decision:
           a. Build ready set: all arrived, unvisited processes.
           b. Select process with minimum priority value.
           c. Tie-break by arrival_time (FCFS).
           d. Execute to completion.

    Formulas:
        p* = argmin{priorityᵢ : pᵢ ∈ ReadyQueue}
        WTᵢ = cᵢ − aᵢ − bᵢ

    Convention:
        priority = 1 → highest priority
        priority = 5 → lowest priority

    Complexity: O(n²)

    """
    processes = sorted(processes, key=lambda p: p.arrival_time)
    n = len(processes)

    current_time = 0
    completed_count = 0
    visited = [False] * n

    schedule = []
    completed = []

    while completed_count < n:
        ready_processes = []

        for i in range(n):
            if not visited[i] and processes[i].arrival_time <= current_time:
                ready_processes.append((i, processes[i]))

        if not ready_processes:
            current_time += 1
            continue

        selected_index, selected_process = min(
            ready_processes,
            key=lambda x: (x[1].priority, x[1].arrival_time)
        )

        start_time = current_time
        end_time = start_time + selected_process.burst_time

        completion_time = end_time
        turnaround_time = completion_time - selected_process.arrival_time
        waiting_time = turnaround_time - selected_process.burst_time
        response_time = start_time - selected_process.arrival_time

        completed.append({
            "pid": selected_process.pid,
            "arrival_time": selected_process.arrival_time,
            "burst_time": selected_process.burst_time,
            "priority": selected_process.priority,
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "response_time": response_time,
        })

        schedule.append((selected_process.pid, start_time, end_time))

        visited[selected_index] = True
        completed_count += 1
        current_time = end_time

    return schedule, completed



def srtf(processes):
    """
    Shortest Remaining Time First (SRTF) Scheduling Algorithm.

    Description:
        The preemptive counterpart to SJF. At every time unit, the
        scheduler evaluates the remaining time of all ready processes
        and selects the one with the smallest remaining burst. If a
        new process arrives with a shorter remaining time than the
        currently executing process, a preemption occurs.

    Algorithm:
        1. Sort processes by arrival time.
        2. At each time unit:
           a. Build ready set: all arrived processes with remaining > 0.
           b. Select process with minimum remaining_time.
           c. Execute for 1 time unit.
           d. Decrement remaining_time.
           e. If remaining = 0: mark completed, compute metrics.
           f. Merge adjacent schedule entries for the same PID.

    Formulas:
        p* = argmin{remaining_timeᵢ : pᵢ ∈ ReadyQueue}
        WTᵢ = cᵢ − aᵢ − bᵢ
        Avg WT is minimized across ALL scheduling algorithms [1]

    Complexity: O(n × Σbᵢ)

            for minimizing average waiting time.
    """
    processes = sorted(processes, key=lambda p: p.arrival_time)
    n = len(processes)

    current_time = 0
    completed_count = 0
    schedule = []
    completed = []

    process_data = []
    for p in processes:
        process_data.append({
            "pid": p.pid,
            "arrival_time": p.arrival_time,
            "burst_time": p.burst_time,
            "priority": p.priority,
            "remaining_time": p.burst_time,
            "start_time": None,
            "completion_time": 0,
        })

    while completed_count < n:
        ready_processes = []

        for p in process_data:
            if p["arrival_time"] <= current_time and p["remaining_time"] > 0:
                ready_processes.append(p)

        if not ready_processes:
            current_time += 1
            continue

        current_process = min(
            ready_processes,
            key=lambda x: (x["remaining_time"], x["arrival_time"])
        )

        if current_process["start_time"] is None:
            current_process["start_time"] = current_time

        start_time = current_time
        end_time = current_time + 1

        if schedule and schedule[-1][0] == current_process["pid"] and schedule[-1][2] == start_time:
            last_pid, last_start, _ = schedule[-1]
            schedule[-1] = (last_pid, last_start, end_time)
        else:
            schedule.append((current_process["pid"], start_time, end_time))

        current_process["remaining_time"] -= 1
        current_time += 1

        if current_process["remaining_time"] == 0:
            current_process["completion_time"] = current_time
            turnaround_time = current_process["completion_time"] - current_process["arrival_time"]
            waiting_time = turnaround_time - current_process["burst_time"]
            response_time = current_process["start_time"] - current_process["arrival_time"]

            completed.append({
                "pid": current_process["pid"],
                "arrival_time": current_process["arrival_time"],
                "burst_time": current_process["burst_time"],
                "priority": current_process["priority"],
                "start_time": current_process["start_time"],
                "completion_time": current_process["completion_time"],
                "waiting_time": waiting_time,
                "turnaround_time": turnaround_time,
                "response_time": response_time,
            })

            completed_count += 1

    return schedule, completed
