import os
from google import genai
from google.genai import types

class GeminiProvider:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.5-pro"

    def generate_stream(self, history):
        try:
            # Adaptar el historial al formato estricto de Gemini
            formatted_contents = []
            for msg in history:
                # Gemini usa los roles 'user' o 'model'
                role = "user" if msg["role"] == "user" else "model"
                formatted_contents.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
                )
            
            # Nueva API `models.generate_content_stream` de google-genai
            response_stream = self.client.models.generate_content_stream(
                model=self.model,
                contents=formatted_contents
            )
            
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise Exception(f"Error de conectividad/API en Google Gemini: {str(e)}")