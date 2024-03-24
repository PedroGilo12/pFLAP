import tkinter as tk

class MultipleRunScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.overrideredirect(True)
        self.geometry("600x828+1149+143")
        self.configure(bg="#333333")

        self.label_input = tk.Label(self, text="Input", bg="#C0C0C0", fg="black", width=53, borderwidth=1, relief="solid")
        self.label_input.place(relx=0.2, rely=0, anchor="n")

        self.label_output = tk.Label(self, text="Output", bg="#C0C0C0", fg="black", width=53, borderwidth=1, relief="solid")
        self.label_output.place(relx=0.8, rely=0, anchor="n")
        
        self.button_close = tk.Button(self, text="X", bg="red", fg="white", command=self.fechar_tela)
        self.button_close.place(relx=1, rely=0.012, anchor="e")

        self.entradas = []
        self.labels = []

        # Cria uma entrada de texto inicial


    def fechar_tela(self):
        self.destroy()



# Cria a janela principal
janela = tk.Tk()
janela.title("Line Edits e Labels Dinâmicos")

# Botão para abrir a tela de múltiplas execuções
def abrir_multiplas_execucoes():
    MultipleRunScreen(janela)

botao_multiplas_execucoes = tk.Button(janela, text="Abrir Tela de Múltiplas Execuções", command=abrir_multiplas_execucoes)
botao_multiplas_execucoes.pack()

# Inicia o loop principal da janela
janela.mainloop()





# class MultipleRunScreen(ctk.CTkToplevel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.overrideredirect(True)
#         self.geometry("480x662+1149+143")
#         self.configure(bg="#333333")
        
#         self.label_input = ctk.CTkLabel(self, text="Output", bg_color="black", fg_color="white", width=20)
#         self.label_input.pack(padx=0, pady=0, side="left")

#         # self.label_output = ctk.CTkLabel(self, text="Output", bg="#C0C0C0", fg="black", width=20, borderwidth=1, relief="solid")
#         # self.label_output.place(relx=0.5, rely=0.9, anchor="s")
    
#     def fechar_tela(self):
#         self.destroy()