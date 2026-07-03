class GeminiClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Gemini is not configured. Using local AI workflow."
        return prompt
