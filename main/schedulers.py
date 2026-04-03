def fcfs(processes):
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


