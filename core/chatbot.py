import sys
from .conversation import ConversationHistory
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider
from providers.gemini_provider import GeminiProvider

class FallbackChatbot:
    def __init__(self):
        self.history = ConversationHistory()
        
        # REQUISITO: Respuesta preconfigurada para fallo total
        self.FALLBACK_MESSAGE = (
            "Lo siento, en este momento todos mis sistemas de IA están fuera de servicio. "
            "He registrado este incidente y podré ayudarte en cuanto se restablezca la conexión."
        )
        
        # Orden de prioridad (Cascada)
        self.providers = [
            ("OpenAI", OpenAIProvider()),
            ("Anthropic", AnthropicProvider()),
            ("Google Gemini", GeminiProvider())
        ]

    def ask(self, user_input):
        # 1. Registrar mensaje del usuario en el historial
        self.history.add_user_message(user_input)
        
        full_response = ""
        success = False
        
        # 2. Intentar cascada de proveedores
        for name, provider in self.providers:
            try:
                print(f"\n[{name}] respondiendo...")
                
                # Obtener el generador del stream
                stream = provider.generate_stream(self.history.get_history())
                
                # Procesamiento de streaming
                for chunk in stream:
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    full_response += chunk
                
                success = True
                print()  # Salto de línea tras finalizar el stream con éxito
                break    
                
            except Exception as e:
                print(f"\n[!] Fallo detectado en {name}: {str(e)}")
                if name != "Google Gemini": # No avisar de fallback si es el último
                    print("[!] Iniciando fallback automático al siguiente proveedor...\n")
                full_response = "" 
                continue
        
        # 3. Lógica de cierre de respuesta
        if success:
            # Caso exitoso: guardar lo que respondió el proveedor
            self.history.add_assistant_message(full_response)
        else:
            # REQUISITO: Si todos fallan, usar respuesta preconfigurada
            print(f"\n[Asistente]: {self.FALLBACK_MESSAGE}")
            # Guardar la respuesta preconfigurada en el historial para mantener la continuidad
            self.history.add_assistant_message(self.FALLBACK_MESSAGE)

    def get_history_summary(self):
        """Opcional: para debug o mostrar cuántos mensajes hay"""
        return len(self.history.get_history())