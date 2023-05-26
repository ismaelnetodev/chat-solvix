import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import script

class InterfaceApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Interface com Tkinter")
        self.root.geometry("400x300")
        self.is_recording = False

        # Carregar e redimensionar o ícone do microfone
        self.microphone_icon = Image.open("imgs\microphone.png") 
        
        self.microphone_button = tk.Button(root, image=self.microphone_icon, command=self.toggle_recording)
        self.microphone_button.grid(row=0, column=0, padx=10, pady=10)

        # Campo de texto
        self.text_box = tk.Text(root, height=10, width=40)
        self.text_box.grid(row=1, column=0, padx=10, pady=10)

    def toggle_recording(self):
        self.is_recording = not self.is_recording

        if self.is_recording:
            script.reconhecimentodeFala()
            messagebox.showinfo("Ouvindo...", "Fale agora!")

            # Faça a ação de início da gravação aqui
        else:
            messagebox.showinfo("Concluindo...", "Enviando para reconhecimento...")
            # Faça a ação de parar a gravação aqui

        # Exemplo de adição de texto ao campo de texto
        received_text = script.answer
        self.text_box.insert(tk.END, received_text + "\n")
        self.text_box.see(tk.END)  # Rolagem automática para o final do campo de texto


root = tk.Tk()
app = InterfaceApp(root)
root.mainloop()