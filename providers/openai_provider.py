import os
from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # Tal como indica el ejercicio, usamos un modelo gpt-4o o similar
        self.model = "gpt-4o" 

    def generate_stream(self, history):
        try:
            # Transformamos el historial al formato 'input' requerido por la API Responses
            # Cada elemento debe especificar su tipo de contenido
            formatted_input = []
            for msg in history:
                formatted_input.append({
                    "role": msg["role"],
                    "content": [{"type": "input_text", "text": msg["content"]}]
                })

            # Llamada correcta usando 'input' y la API de Responses
            stream = self.client.responses.create(
                model=self.model,
                input=formatted_input,
                stream=True
            )

            # En la API Responses, el streaming devuelve eventos. 
            # Buscamos el evento 'response.text.delta'
            for event in stream:
                if event.type == "response.text.delta":
                    yield event.delta
                    
        except Exception as e:
            raise Exception(f"Error en OpenAI (Responses API): {str(e)}")