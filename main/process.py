from dataclasses import dataclass

@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0



