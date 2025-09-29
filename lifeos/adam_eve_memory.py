from collections import deque
from typing import Any, Dict, List


class RingMemory:
    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.data = deque(maxlen=capacity)

    def remember(self, gen: int, event: Dict[str, Any]):
        self.data.append({"gen": gen, **event})

    def recall(self) -> List[Dict[str, Any]]:
        return list(self.data)

class SharedLedger:
    def __init__(self, cap_bytes: int = 16 * 1024):
        self.capacity_bytes = cap_bytes   # <-- rename to capacity_bytes
        self.used_bytes = 0
        self.events: List[dict] = []

    def add(self, event: dict):
        event_size = len(str(event).encode("utf-8"))
        if self.used_bytes + event_size <= self.capacity_bytes:
            self.events.append(event)
            self.used_bytes += event_size
