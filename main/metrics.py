def calculate_averages(completed):
    n = len(completed)

    avg_waiting = sum(p["waiting_time"] for p in completed) / n
    avg_turnaround = sum(p["turnaround_time"] for p in completed) / n
    avg_response = sum(p["response_time"] for p in completed) / n

    total_time = max(p["completion_time"] for p in completed) - min(p["arrival_time"] for p in completed)
    throughput = n / total_time if total_time > 0 else 0

    return {
        "avg_waiting_time": avg_waiting,
        "avg_turnaround_time": avg_turnaround,
        "avg_response_time": avg_response,
        "throughput": throughput
    }