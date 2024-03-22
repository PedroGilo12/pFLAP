import tkinter as tk
from PIL import Image, ImageTk

class TelaComBotoes(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.criar_widgets()

    def criar_widgets(self):
        # Adicionando label azul
        self.label_azul = tk.Label(self, bg="blue", width=50, height=720)  # Definindo o tamanho da label
        self.label_azul.grid(row=0, column=0)
        
        # Calculando as coordenadas para posicionar o botão no centro da label
        x_centro = 50 // 2
        y_centro = 720 // 2
        
        # Adicionando o botão ao centro da label
        self.botao = tk.Button(self.label_azul, text="Botão", height=5, width=10, font=("Helvetica", 12))  # Ajustando a fonte
        self.botao.place(x=x_centro, y=y_centro, anchor="center")  # Posicionando o botão no centro da label

# Criando a aplicação principal
root = tk.Tk()
root.title("Tela com Botões e Imagem")
root.geometry("400x720")

# Criando e mostrando a tela com botões
tela = TelaComBotoes(master=root)
tela.mainloop()
