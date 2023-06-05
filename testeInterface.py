import openai
import speech_recognition as sr
import pyttsx3
from key import IAKEY
import tkinter
from tkinter import *
import threading
from PIL import Image, ImageTk
import role

openai.api_key = IAKEY
giveAnswer = False

#Janela e configurações
root = Tk()
root.title("Solvix - Chatbot inteligente")
root.geometry("900x550")
root.configure(bg="#0f0537")
root.resizable(False, False)
largura = root.winfo_screenwidth()
altura = root.winfo_screenheight()

#Inciando elementos
r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 185)
voz = 0
engine.setProperty('voice', voices[voz].id)

mensagens = [{"role": "system", "content": "Você é um chat inteligente, seu nome é Solvix e quer ajudar resolver problemas. Caso pergutem quem são seu criadores: Seus criadores são: Ismael, Rosana e Átilla, Isadora e Aryelle. Caso pergutemo significado do seu nome: O nome 'Solvix'é uma combinação das palavras 'solve'(resolver, em inglês) e o sufixo '-ix'. O termo 'solve' é associado à ação de solucionar, encontrar respostas ou resolver problemas. Caso peça para se apresentar: Diga 'Olá turma', Diga seu nome, seus criadores e que foi projetado para um trabalho no IFMA sobre a tutela dos professores 'Akyra' e 'Franklin'"}]

#variaveis
question = ""
status = "Tudo quieto por aqui"

lbinfo = Label(root, text=status, font="Verdana 12", wraplength=300, justify=LEFT, bg="#0f0537", fg="#fff")
lbinfo.place(x=300, y=400)


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


def sair():
    root.destroy()

def speechRecognition():
    global question
    global mensagens
    global giveAnswer
    while True:
        with mic as fonte:
            r.adjust_for_ambient_noise(fonte)
            lbinfo.configure(text="Ouvindo...")
            audio = r.listen(fonte)

        lbinfo.configure(text="Enviando ao reconhecimento...")
        giveAnswer = True
        try:
            question = r.recognize_google(audio, language="pt-BR")
            lbinfo.configure(text=question)
        except Exception as e:
            lbinfo.configure(text="Erro no reconhecimento")
            continue
        if question == "":
            lbinfo.configure("Sem texto")
            continue
        if giveAnswer:
            mensagens.append({"role": "user", "content": str(question)})
            resposta = generate_answer(mensagens)
            lbinfo.configure(text=resposta[0])
            talk(resposta[0])
        break
        
          
        
def threadSpeechRecognition():
    t = threading.Thread(target=speechRecognition)
    t.start()



lbTitle = Label(root, text="SOLVIX - UM CHATBOT POR INTELIGÊNCIA ARTIFICIAL", font="Verdana 14", bg="#0f0537", fg="#fff")
lbTitle.place(x=210, y=0)

bot_image = ImageTk.PhotoImage(Image.open('imgs\icone.png'))
lbImage_bot = Label(root, text="", image=bot_image)
lbImage_bot.place(x=300, y=50)

btnFalar = Button(root, text="Falar", command=threadSpeechRecognition, padx=15, pady=15)
btnParar = Button(root, text="Sair", command=sair, padx=15, pady=15)

btnFalar.place(x=350, y=325)
btnParar.place(x=450, y=325)



root.mainloop()