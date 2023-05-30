import openai
import speech_recognition as sr
import pyttsx3
from key import IAKEY
import tkinter
from tkinter import *
import threading
from PIL import Image, ImageTk

openai.api_key = IAKEY

#Janela e configurações
root = Tk()
root.title("Solvix - Chatbot inteligente")
root.geometry("600x500")
root.configure(bg="#011901")
root.resizable(False, False)

#Inciando elementos
r = sr.Recognizer()
mic = sr.Microphone()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 185)
voz = 0
engine.setProperty('voice', voices[voz].id)

#variaveis
question = ""
status = "Tudo quieto por aqui"

lbinfo = Label(root, text=status, font="Verdana 12")
lbinfo.grid(row=2, column=1, columnspan=1)

def speechRecognition():
    global question
    while True:
        with mic as fonte:
            r.adjust_for_ambient_noise(fonte)
            lbinfo.configure(text="Ouvindo...")
            audio = r.listen(fonte)

        lbinfo.configure(text="Enviando ao reconhecimento...")
        
        try:
            question = r.recognize_google(audio, language="pt-BR")
            lbinfo.configure(text=question)
        except Exception as e:
            lbinfo.configure(text="Erro no reconhecimento")
            continue
        if question == "":
            lbinfo.configure("Sem texto")
            continue
        break
          
        
def threadSpeechRecognition():
    t = threading.Thread(target=speechRecognition)
    t.start()



lbTitle = Label(root, text="SOLVIX - UM CHATBOT POR INTELIGÊNCIA ARTIFICIAL", font="Verdana 14")
lbTitle.grid(row=0, column=0, columnspan=3)

bot_image = ImageTk.PhotoImage(Image.open('imgs\img_bot.png'))
lbImage_bot = Label(root, text="", image=bot_image)
lbImage_bot.grid(row=1, column=0, sticky=W)

btnFalar = Button(root, text="Falar", command=threadSpeechRecognition, padx=15, pady=15)
btnParar = Button(root, text="Parar", padx=15, pady=15)

btnFalar.grid(row=1, column=1)
btnParar.grid(row=1, column=2)



root.mainloop()