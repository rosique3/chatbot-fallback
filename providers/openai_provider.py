import os
from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Usa el modelo que prefieras de la familia reciente
        self.model = "gpt-4o" 

    def generate_stream(self, history):
        try:
            # Uso de la API de Responses en lugar de Chat Completions
            stream = self.client.responses.create(
                model=self.model,
                messages=history,
                stream=True
            )
            for chunk in stream:
                # Estructura genérica que suele usarse para mapear el stream
                if getattr(chunk, 'choices', None) and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
        except Exception as e:
            raise Exception(f"Error de conectividad/API en OpenAI: {str(e)}")