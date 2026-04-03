from process import Process



def scenario_basic():
    return [
        Process("P1", arrival_time=0, burst_time=5, priority=2),
        Process("P2", arrival_time=1, burst_time=3, priority=1),
        Process("P3", arrival_time=2, burst_time=8, priority=3),
        Process("P4", arrival_time=3, burst_time=6, priority=2),
    ]


def scenario_convoy_effect():
    return [
        Process("P1", arrival_time=0, burst_time=20, priority=3),
        Process("P2", arrival_time=1, burst_time=2, priority=1),
        Process("P3", arrival_time=2, burst_time=2, priority=1),
        Process("P4", arrival_time=3, burst_time=2, priority=2),
        Process("P5", arrival_time=4, burst_time=2, priority=2),
    ]


def scenario_rr_friendly():
    return [
        Process("P1", arrival_time=0, burst_time=9, priority=3),
        Process("P2", arrival_time=0, burst_time=5, priority=1),
        Process("P3", arrival_time=0, burst_time=7, priority=2),
        Process("P4", arrival_time=0, burst_time=3, priority=1),
        Process("P5", arrival_time=0, burst_time=1, priority=2),
    ]


def scenario_priority_case():
    return [
        Process("P1", arrival_time=0, burst_time=8, priority=3),
        Process("P2", arrival_time=1, burst_time=4, priority=1),
        Process("P3", arrival_time=2, burst_time=9, priority=5),
        Process("P4", arrival_time=3, burst_time=5, priority=2),
        Process("P5", arrival_time=4, burst_time=2, priority=4),
    ]


def scenario_srtf_case():
    return [
        Process("P1", arrival_time=0, burst_time=12, priority=3),
        Process("P2", arrival_time=2, burst_time=2, priority=1),
        Process("P3", arrival_time=4, burst_time=1, priority=2),
        Process("P4", arrival_time=6, burst_time=3, priority=2),
        Process("P5", arrival_time=8, burst_time=2, priority=1),
    ]


def scenario_presentation():
    return [
        Process("P1", arrival_time=0, burst_time=15, priority=4),
        Process("P2", arrival_time=1, burst_time=3, priority=1),
        Process("P3", arrival_time=2, burst_time=6, priority=3),
        Process("P4", arrival_time=3, burst_time=1, priority=2),
        Process("P5", arrival_time=4, burst_time=8, priority=5),
        Process("P6", arrival_time=5, burst_time=4, priority=2),
    ]