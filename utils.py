import random


def chance(percent: float) -> bool:
    return random.uniform(0, 100) <= max(0, min(100, percent))
