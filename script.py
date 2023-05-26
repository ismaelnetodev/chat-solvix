import openai  # pip install openai
import speech_recognition as sr  # pip install SpeechRecognition
from key import IAKEY
import whisper  # pip install whisper-openai
from funcoes import *
import pyttsx3  # pip install pyttsx3
import os

# Initialize the API key
openai.api_key = IAKEY

# caso nao queira falar "assistente" ou "Chat GPT"
sem_palavra_ativadora = False
# printa o total de tokens por interacao
debug_custo = False
# print de algumas informacoes para debug
debugar = False
# define qual gerador de texto
# escolher_stt = "whisper"
escolher_stt = "google"
# escolhe entrada por texto ou voz
entrada_por_texto = False
# falar ou nao
falar = True
ativar_fala = False

if entrada_por_texto:
    sem_palavra_ativadora = True


def generate_answer(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  ##
        # model="gpt-3.5-turbo-0301", ## ateh 1 junho 2023
        messages=messages,
        max_tokens=1000,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


def talk(texto):
    # falando
    engine.say(texto)
    engine.runAndWait()
    engine.stop()


def save_file(dados):
    with open(path + filename, "wb") as f:
        f.write(dados)
        f.flush()


# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()
model = whisper.load_model("base")

# falar
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)  # velocidade 120 = lento
for indice, vozes in enumerate(voices):  # listar vozes
    print(indice, vozes.name)
voz = 0  
engine.setProperty('voice', voices[voz].id)

mensagens = [{"role": "system", "content": "Você é um assistente inteligente, seu nome é Solvix e quer ajudar resolver problemas. Seus criadores são: Ismael, Rosana e Átilla"}]

path = os.getcwd()
filename = "audio.wav"

print("Speak to Text", escolher_stt)

ajustar_ambiente_noise = True

while True:
    text = ""
    question = ""

    if entrada_por_texto:
        question = input("Digite o que quizer (\"sair\"): ")
    else:
        # Ask a question
        with mic as fonte:
            if ajustar_ambiente_noise:
                r.adjust_for_ambient_noise(fonte)
                ajustar_ambiente_noise = False
            print("Fale alguma coisa")
            audio = r.listen(fonte)
            print("Enviando para reconhecimento")

            if escolher_stt == "google":
                try:
                    question = r.recognize_google(audio, language="pt-BR")
                except Exception as e:
                    print("Erro no reconhecimento")
                    continue
            elif escolher_stt == "whisper":
                save_file(audio.get_wav_data())

        if escolher_stt == "whisper":
            text = model.transcribe(path + filename, language='pt', fp16=False)
            question = text["text"]

    if ("desligar" in question and "assistente" in question) or question.startswith("sair"):
        print(question, "Saindo.")
        if falar:
            talk("Desligando")
        break
    elif question == "":
        print("No sound")
        continue
    elif question.startswith("Assistente") or question.startswith("assistente") or question.startswith(
            "solvix") or sem_palavra_ativadora:
        print("Me: ", question)
        mensagens.append({"role": "user", "content": str(question)})

        answer = generate_answer(mensagens)

        print("Solvix:", answer[0])

        if debug_custo:
            print("Cost:\n", answer[1])

        mensagens.append({"role": "assistant", "content": answer[0]})

        if falar:
            talk(answer[0])
    else:
        print("No message")
        continue

    if debugar:
        print("Mensages", mensagens, type(mensagens))
print("See ya!")