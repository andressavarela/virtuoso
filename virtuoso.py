import speech_recognition as sr
import wave
import pyaudio
from gtts import gTTS
import os
import time
import serial

# Configurações do dispositivo de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Taxa de amostragem (exemplo de 16 kHz)
CHUNK = 1024  # Tamanho do buffer

while True:  # Loop externo para continuar rodando
    recognized = False
    text_entry = ""

    while not recognized:
        # Inicializa o objeto PyAudio
        audio = pyaudio.PyAudio()

        # Abre o stream de áudio
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Aguardando comando 'ei assistente' ou 'assistente'...")

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
        languageCode = "pt-BR"
        try:
            # Lê o áudio do arquivo gravado
            with sr.AudioFile("audio-input.wav") as source:
                audio_data = recognizer.record(source)

            # Reconhece a fala usando o Google Web Speech API
            text_entry = recognizer.recognize_google(
                audio_data, language=languageCode)
            print("Texto reconhecido: " + text_entry)
            recognized = True

        except sr.UnknownValueError:
            print("Nao foi possível reconhecer a fala.")
        except sr.RequestError as e:
            print(
                "Erro no request ao Google Web Speech API: {0}".format(e))

        if text_entry.lower().startswith(("ei assistente", "assistente")):
            # Responde "Ao seu dispor"

            print("Ao seu dispor")

            # Inicia nova gravação para a pergunta

            text_entry = ""

            # Inicializa o objeto PyAudio para a nova gravação
            audio = pyaudio.PyAudio()

            # Abre o stream de áudio
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)

            print("Aguardando comando")

            frames = []

            # Grava áudio por um determinado período (por exemplo, 5 segundos)
            for _ in range(0, int(RATE / CHUNK * 5)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("Nova gravação concluída.")

            # Para a gravação
            stream.stop_stream()
            stream.close()

            # Fecha o objeto PyAudio
            audio.terminate()

            # Salva a gravação em um arquivo WAV
            with wave.open("question.wav", "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))

            # Inicializa o reconhecedor de fala
            recognizer = sr.Recognizer()

            try:
                # Lê o áudio do arquivo gravado
                with sr.AudioFile("question.wav") as source:
                    audio_data = recognizer.record(source)

                # Reconhece a fala usando o Google Web Speech API
                text_entry = recognizer.recognize_google(
                    audio_data, language=languageCode)
                print("Texto reconhecido: " + text_entry)

            except sr.UnknownValueError:
                print("Nao foi possível reconhecer a fala.")
            except sr.RequestError as e:
                print(
                    "Erro no request ao Google Web Speech API: {0}".format(e))

            ai_answer = ""

            arduino_port = 'COMX'  # Substitua 'COMX' pela porta serial correta
            # 9600 é a taxa de baud do Arduino
            ser = serial.Serial(arduino_port, 9600)

            if text_entry.lower().startswith(("quem é você", "o que é você", "o que você é")):
                ai_answer = "Sou um protótipo de chatbot criado para te auxiliar em simples tarefas e perguntas"
            elif text_entry.lower().startswith(("quem te fez", "quem te criou", "da onde você surgiu")):
                ai_answer = "Fui desenvolvido pelos estudantes Igor Marques e Andressa Varela, como projeto para a APS de Microcontroladores e IOT"
            elif text_entry.lower().startswith(("Tudo bem?", "tudo bom?", "Como você tá?")):
                ai_answer = "Tudo está nos conformes do esperado para um programa incompetente como eu"
            elif text_entry.lower().startswith(("que horas são", "que horas é", "são que horas agora?")):
                current_time = time.strftime("%H:%M")
                ai_answer = f"Agora são {current_time}"
            elif text_entry.lower().startswith(("acenda a lâmpada", "luz acesa", "acende")):
                ser.write(b'L')
                ai_answer = "Lâmpada ligada"
            elif text_entry.lower().startswith(("apague a lâmpada", "luz apagada", "desliga", "apaga")):
                ser.write(b'D')
                ai_answer = "Lâmpada desligada"

            # Idioma da resposta a ser reproduzida
            language = 'pt'

            # Ao transmitir o texto e idioma à API, marcamos
            # slow=False. O que significa que o módulo de
            # áudio terá uma velocidade maior.

            myobj = gTTS(text=ai_answer, lang=language, slow=False)

            # Salva o áudio convertido em um arquivo chamado
            # output
            myobj.save("audio-output.mp3")

            # Reproduzindo o arquivo convertido
            os.system("audio-output.mp3")

        else:
            language = 'pt'
            print("Comando não reconhecido: " + text_entry)

            print("Não foi possível efetuar a pesquisa")
