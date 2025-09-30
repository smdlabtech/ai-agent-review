from __future__ import annotations
import os
from typing import List, Dict
import google.generativeai as genai

class GeminiProvider:
    def __init__(self, model: str = "gemini-1.5-flash") -> None:
        self.model = model
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.client = genai.GenerativeModel(self.model)

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Concatenate messages into a single prompt for simplicity
        prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
        resp = self.client.generate_content(prompt)
        return resp.text.strip() if getattr(resp, "text", None) else "No response."