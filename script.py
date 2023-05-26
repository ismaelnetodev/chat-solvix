import openai  # pip install openai
import speech_recognition as sr  # pip install SpeechRecognition
from key import IAKEY
import pyttsx3  # pip install pyttsx3
import os
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Initialize the API key
openai.api_key = IAKEY

# printa o total de tokens por interacao
debug_custo = False
# print de algumas informacoes para debug
debugar = False
escolher_stt = "google"

# falar ou nao
falar = True
ativar_fala = False

window = Tk()
window.title("Solvix - chatbot inteligente")
window.geometry("500x400")


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

# reconhecer
r = sr.Recognizer()
mic = sr.Microphone()

#falar
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 180)  # velocidade 120 = lento
for indice, vozes in enumerate(voices):  # listar vozes
    print(indice, vozes.name)
voz = 0  
engine.setProperty('voice', voices[voz].id)

mensagens = [{"role": "system", "content": "Você é um chat inteligente, seu nome é Solvix e quer ajudar resolver problemas. Caso pergutem quem são seu criadores: Seus criadores são: Ismael, Rosana e Átilla, Isadora e Aryelle. Caso pergutemo significado do seu nome: O nome 'Solvix'é uma combinação das palavras 'solve'(resolver, em inglês) e o sufixo '-ix'. O termo 'solve' é associado à ação de solucionar, encontrar respostas ou resolver problemas. Caso peça para se apresentar: Diga 'Olá turma', Diga seu nome, seus criadores e que foi projetado para um trabalho no IFMA sobre a tutela dos professores 'Akyra' e 'Franklin'"}]

print("Speak to Text", escolher_stt)
def reconhecerFala():
    ajustar_ambiente_noise = True

    while True:
        text = ""
        question = ""
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

        if ("desligar" in question and "assistente" in question) or question.startswith("sair"):
            print(question, "Saindo.")
            if falar:
                talk("Desligando")
            break
        elif question == "":
            print("No sound")
            continue
        
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


botao = Button(window, text="Falar", command=reconhecerFala)
botao.pack()

window.mainloop()