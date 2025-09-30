from .provider_openai import OpenAIProvider
from .provider_gemini import GeminiProvider

class ProviderFactory:
    @staticmethod
    def create(name: str, model: str):
        name = (name or "").lower()
        if name == "openai":
            return OpenAIProvider(model=model)
        return GeminiProvider(model=model)