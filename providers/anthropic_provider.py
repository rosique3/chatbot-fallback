import os
from anthropic import Anthropic

class AnthropicProvider:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-7-sonnet-latest"

    def generate_stream(self, history):
        try:
            # Transformamos el historial genérico al formato estricto de bloques de Anthropic
            formatted_messages = []
            for msg in history:
                formatted_messages.append({
                    "role": msg["role"], # Anthropic también usa "user" y "assistant"
                    "content": [{"type": "text", "text": msg["content"]}]
                })

            # Uso del context manager de streaming con los mensajes ya formateados
            with self.client.messages.stream(
                max_tokens=1024,
                messages=formatted_messages,
                model=self.model,
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            raise Exception(f"Error de conectividad/API en Anthropic: {str(e)}")