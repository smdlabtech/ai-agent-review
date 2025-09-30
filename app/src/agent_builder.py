from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

from .memory_module import Memory
from .planner import ReactivePlanner
from .providers import ProviderFactory

load_dotenv()

@dataclass
class SmartAgentConfig:
    tools: List[str] = field(default_factory=list)
    memory: str = "short_term"
    planner: str = "reactive"
    system_prompt: str = (
        "You are a helpful, concise AI agent. "
        "Always justify tool usage briefly and cite sources when possible."
    )
    provider_name: Optional[str] = None
    model: Optional[str] = None

class SmartAgent:
    def __init__(self, tools: List[str], memory: str = "short_term",
                 planner: str = "reactive", system_prompt: Optional[str] = None,
                 provider_name: Optional[str] = None, model: Optional[str] = None) -> None:
        cfg = SmartAgentConfig(
            tools=tools, memory=memory, planner=planner,
            system_prompt=system_prompt or SmartAgentConfig.system_prompt,
            provider_name=provider_name or os.getenv("MODEL_PROVIDER", "gemini"),
            model=model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        )
        self.config = cfg
        self.memory = Memory(mode=cfg.memory)
        self.planner = ReactivePlanner()
        self.llm = ProviderFactory.create(cfg.provider_name, cfg.model)

    def run(self, user_query: str) -> str:
        context = self.memory.recall(k=5)
        plan = self.planner.plan(user_query, context=context, tools=self.config.tools)
        # Execute plan naively (no tools implemented for brevity)
        prompt = [
            {"role": "system", "content": self.config.system_prompt},
            {"role": "user", "content": user_query},
            {"role": "user", "content": f"[context]: {context}"},
            {"role": "user", "content": f"[plan]: {plan}"},
        ]
        reply = self.llm.chat(prompt)
        self.memory.store({"query": user_query, "reply": reply})
        return reply