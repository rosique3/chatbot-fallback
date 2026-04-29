import os
from openai import OpenAI

class OpenAIProvider:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o" 

    def generate_stream(self, history):
        try:
            formatted_input = []
            for msg in history:
                formatted_input.append({
                    "role": msg["role"],
                    "content": [{"type": "input_text", "text": msg["content"]}]
                })

            stream = self.client.responses.create(
                model=self.model,
                input=formatted_input,
                stream=True
            )

            for event in stream:
                # Verificamos que sea el evento de delta de texto
                if event.type == "response.text.delta":
                    # Extraemos específicamente el texto del objeto delta.
                    # Dependiendo de la versión exacta del SDK, suele ser .text o .output_text
                    text_chunk = getattr(event.delta, 'text', getattr(event.delta, 'output_text', ''))
                    
                    if text_chunk:
                        yield text_chunk
                        
        except Exception as e:
            raise Exception(f"Error en OpenAI (Responses API): {str(e)}")