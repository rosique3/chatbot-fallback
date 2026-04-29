import os
from dotenv import load_dotenv
from core.chatbot import FallbackChatbot

def main():
    # Cargar variables de entorno (las API keys del archivo .env)
    load_dotenv()
    
    print("="*60)
    print("Iniciando Chatbot Inteligente con Sistema de Fallback")
    print("Cascada: OpenAI -> Anthropic Claude -> Google Gemini")
    print("Escribe '/salir' para terminar la conversación de forma limpia.")
    print("="*60)
    
    chatbot = FallbackChatbot()
    
    while True:
        try:
            user_input = input("\nTú: ")
            
            # Salida limpia si el usuario escribe la instrucción
            if user_input.strip().lower() == "/salir":
                print("Saliendo de la interfaz conversacional. ¡Hasta luego!")
                break
            
            # Evitar enviar mensajes vacíos a la API
            if not user_input.strip():
                continue
                
            chatbot.ask(user_input)
            
        except KeyboardInterrupt:
            # Manejo de cierre forzado con Control + C
            print("\nSaliendo de la interfaz conversacional. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()