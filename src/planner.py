from __future__ import annotations
from typing import Any, Dict, List

class ReactivePlanner:
    def plan(self, query: str, context: List[Any], tools: List[str]) -> Dict[str, Any]:
        return {
            "strategy": "reactive",
            "steps": [
                {"type": "analyze", "desc": "Understand the user intent"},
                {"type": "respond", "desc": "Draft a concise and helpful answer"},
            ],
            "tools_available": tools,
        }