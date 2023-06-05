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

#variaveis
question = ""
status = "Tudo quieto por aqui"

lbinfo = Label(root, text=status, font="Verdana 12", wraplength=300, justify=LEFT, bg="#0f0537", fg="#fff")
lbinfo.place(x=300, y=400)

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



lbTitle = Label(root, text="SOLVIX - UM CHATBOT POR INTELIGÊNCIA ARTIFICIAL", font="Verdana 14", bg="#0f0537", fg="#fff")
lbTitle.place(x=210, y=0)

bot_image = ImageTk.PhotoImage(Image.open('imgs\icone.png'))
lbImage_bot = Label(root, text="", image=bot_image)
lbImage_bot.place(x=300, y=50)

btnFalar = Button(root, text="Falar", command=threadSpeechRecognition, padx=15, pady=15)
btnParar = Button(root, text="Parar", padx=15, pady=15)

btnFalar.place(x=350, y=325)
btnParar.place(x=450, y=325)



root.mainloop()