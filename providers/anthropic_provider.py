import os
from anthropic import Anthropic

class AnthropicProvider:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-7-sonnet-latest"

    def generate_stream(self, history):
        try:
            # Anthropic usa su propio contexto de streaming context manager
            with self.client.messages.stream(
                max_tokens=1024,
                messages=history,
                model=self.model,
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            raise Exception(f"Error de conectividad/API en Anthropic: {str(e)}")