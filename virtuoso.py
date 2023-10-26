import speech_recognition as sr
import wave
import pyaudio
from gtts import gTTS
import os
import time
import serial

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

while True:
    recognized = False
    text_entry = ""

    while not recognized:
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Aguardando comando 'ei virtuoso' ou 'virtuoso'...")

        frames = []

        for _ in range(0, int(RATE / CHUNK * 5)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Gravação concluída.")

        stream.stop_stream()
        stream.close()

        audio.terminate()

        with wave.open("audio-input.wav", "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(frames))

        recognizer = sr.Recognizer()
        languageCode = "pt-BR"
        try:
            with sr.AudioFile("audio-input.wav") as source:
                audio_data = recognizer.record(source)

            text_entry = recognizer.recognize_google(
                audio_data, language=languageCode)
            print("Texto reconhecido: " + text_entry)
            recognized = True

        except sr.UnknownValueError:
            print("Nao foi possível reconhecer a fala.")
        except sr.RequestError as e:
            print(
                "Erro no request ao Google Web Speech API: {0}".format(e))

        if text_entry.lower().startswith(("ei virtuoso", "virtuoso", "virtuosa")):

            print("Ao seu dispor")

            text_entry = ""

            audio = pyaudio.PyAudio()

            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)

            print("Aguardando comando")

            frames = []

            for _ in range(0, int(RATE / CHUNK * 5)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("Nova gravação concluída.")

            stream.stop_stream()
            stream.close()

            audio.terminate()

            with wave.open("question.wav", "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(frames))

            recognizer = sr.Recognizer()

            try:

                with sr.AudioFile("question.wav") as source:
                    audio_data = recognizer.record(source)

                text_entry = recognizer.recognize_google(
                    audio_data, language=languageCode)
                print("Texto reconhecido: " + text_entry)

            except sr.UnknownValueError:
                print("Nao foi possível reconhecer a fala.")
            except sr.RequestError as e:
                print(
                    "Erro no request ao Google Web Speech API: {0}".format(e))

            ai_answer = ""

            ser = serial.Serial("COM6", 9600)

            if text_entry.lower().startswith(("quem é você", "o que é você", "o que você é")):
                ai_answer = "Sou um protótipo de chatbot criado para te auxiliar em simples tarefas e perguntas"
            elif text_entry.lower().startswith(("quem te fez", "quem te criou", "da onde você surgiu")):
                ai_answer = "Fui desenvolvido pelos estudantes Igor Marques e Andressa Varela, como projeto para a APS de Microcontroladores e IOT"
            elif text_entry.lower().startswith(("Tudo bem?", "tudo bom?", "Como você tá?")):
                ai_answer = "Tudo está nos conformes do esperado para um programa como eu"
            elif text_entry.lower().startswith(("que horas são", "que horas é", "são que horas agora?")):
                current_time = time.strftime("%H:%M")
                ai_answer = f"Agora são {current_time}"
            elif text_entry.lower().startswith(("acenda a lâmpada", "luz acesa", "acende")):
                ser.write(b'H')
                ai_answer = "Lâmpada ligada"
            elif text_entry.lower().startswith(("apague a lâmpada", "luz apagada", "desliga", "apaga")):
                ser.write(b'L')
                ai_answer = "Lâmpada desligada"

            language = 'pt'

            myobj = gTTS(text=ai_answer, lang=language, slow=False)

            myobj.save("audio-output.mp3")

            os.system("audio-output.mp3")

        else:
            language = 'pt'
            print("Comando não reconhecido: " + text_entry)

            print("Não foi possível efetuar a pesquisa")
