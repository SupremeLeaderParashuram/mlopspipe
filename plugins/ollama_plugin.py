class OllamaPlugin:
    """Converts natural-language intent to structured task config via Ollama."""
    def parse(self, prompt: str) -> dict:
        # Stub — wire up local Ollama HTTP API here
        return {"task": "classification", "target": "label"}
