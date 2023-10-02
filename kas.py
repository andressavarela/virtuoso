from EdgeGPT.EdgeUtils import Query, Cookie
import speech_recognition as sr
import wave
import pyaudio
import asyncio
import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from EdgeGPT.EdgeUtils import Query, Cookie
from gtts import gTTS
import os

# Configurações do dispositivo de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Taxa de amostragem (exemplo de 16 kHz)
CHUNK = 1024  # Tamanho do buffer

# Inicializa o objeto PyAudio
audio = pyaudio.PyAudio()

# Abre o stream de áudio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Gravando...")

frames = []

# Grava áudio por um determinado período (por exemplo, 5 segundos)
for _ in range(0, int(RATE / CHUNK * 5)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Gravação concluída.")

# Para a gravação
stream.stop_stream()
stream.close()

# Fecha o objeto PyAudio
audio.terminate()

# Salva a gravação em um arquivo WAV
with wave.open("audio-input.wav", "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))

# Inicializa o reconhecedor de fala
recognizer = sr.Recognizer()

try:
    # Lê o áudio do arquivo gravado
    with sr.AudioFile("audio-input.wav") as source:
        audio_data = recognizer.record(source)

    # Reconhece a fala usando o Google Web Speech API
    text_entry = recognizer.recognize_google(audio_data)
    print("Texto reconhecido: " + text_entry)

except sr.UnknownValueError:
    print("Nao foi possível reconhecer a fala.")
except sr.RequestError as e:
    print("Erro no request ao Google Web Speech API: {0}".format(e))
    
#se der erro na gravação, ele deve reiniciar a gravação e tentativa de ler o arquivo
    
#CHECAR SE O COMANDO É DA LÂMPADA

#se for, pula a pesquisa no EdgeGPT 

int LED = 12  # Pino onde a lâmpada virtual está conectada

def control_lamp(command):
    if command == "ligar":
        digitalWrite(LED, HIGH)  # Liga a lâmpada
        print("Lâmpada ligada.")
    elif command == "desligar":
        digitalWrite(LED, LOW)  # Desliga a lâmpada
        print("Lâmpada desligada.")
    else:
        print("Comando de voz não reconhecido.")

# Chamada da função de controle da lâmpada
control_lamp(text_entry)

```responde "Luz acesa"
-- fazer lógica de checar se a luz já está acesa e, se sim, perguntar se a pessoa deseja apagar (responde "Luz apagada") 
```

# COMEÇO DO BING AI
ai_answer = ""

async def main():
    global ai_answer
    bot = await Chatbot.create()  
    response = await bot.ask(prompt=text_entry, conversation_style=ConversationStyle.creative, simplify_response=True) #Definições como estilo de conversa e resposta simplificada.
    ai_answer = response["text"]
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())

#Efetua a busca 
q = Query(
    text_entry,
    style="creative",  # ou: 'balanced', 'precise'
    cookie_files="./bing_cookies_.json"
)

#Exibe a resposta
print(ai_answer)

# Idioma da resposta a ser reproduzida

language = 'en'
  
# Ao transmitir o texto e idioma à API, marcamos 
# slow=False. O que significa que o módulo de
# áudio terá uma velocidade maior. 

myobj = gTTS(text=ai_answer, lang=language, slow=False)
  
# Salva o áudio convertido em um arquivo chamado
# output 
myobj.save("audio-output.mp3")
  
# Reproduzindo o arquivo convertido
os.system("audio-output.mp3")
