from __future__ import annotations
from collections import deque
from typing import Any, Deque, List

class Memory:
    def __init__(self, mode: str = "short_term", max_items: int = 20) -> None:
        self.mode = mode
        self.buffer: Deque[Any] = deque(maxlen=max_items if mode == "short_term" else 200)

    def store(self, item: Any) -> None:
        self.buffer.append(item)

    def recall(self, k: int = 5) -> List[Any]:
        return list(self.buffer)[-k:]