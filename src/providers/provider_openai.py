from __future__ import annotations
import os
from typing import List, Dict, Any
from openai import OpenAI

class OpenAIProvider:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Convert to OpenAI format
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
            temperature=0.2,
            max_tokens=700,
        )
        return completion.choices[0].message.content.strip()