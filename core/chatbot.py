import sys
from .conversation import ConversationHistory
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.gemini_provider import GeminiProvider

class FallbackChatbot:
    def __init__(self):
        self.history = ConversationHistory()
        
        # Orden de prioridad (Cascada)
        self.providers = [
            ("OpenAI", OpenAIProvider()),
            ("Anthropic", AnthropicProvider()),
            ("Google Gemini", GeminiProvider())
        ]

    def ask(self, user_input):
        self.history.add_user_message(user_input)
        
        full_response = ""
        success = False
        
        for name, provider in self.providers:
            try:
                print(f"\n[{name}] respondiendo...")
                
                # Obtener el generador del stream
                stream = provider.generate_stream(self.history.get_history())
                
                # Iterar sobre los fragmentos que llegan del streaming
                for chunk in stream:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    full_response += chunk
                
                success = True
                print()  # Salto de línea limpio al final del stream
                break    # Si respondió con éxito, rompemos el bucle de fallback
                
            except Exception as e:
                print(f"\n[!] Fallo detectado en {name}: {str(e)}")
                print("[!] Iniciando fallback automático al siguiente proveedor...\n")
                full_response = ""  # Limpiamos si hubo salida parcial antes de fallar
                continue
                
        if success:
            self.history.add_assistant_message(full_response)
        else:
            print("\n[Error Crítico] Todos los proveedores fallaron. Verifica tus API keys, la conexión a internet o los límites de cuota de la API.")