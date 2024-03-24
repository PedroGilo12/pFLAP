import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from customtkinter import filedialog
import os
import pygame
import tela
import JFLAPimport as jf
from CTkMenuBar import *
from tkinter import messagebox

LARGEFONT =("Verdana", 35)

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

        self.button_run = tk.Button(self, text="Run", bg="green", fg="white", command=self.get_entradas)
        self.button_run.place(relx=0.5, rely=0.95, anchor="s")

        self.entradas = []

        self.adicionar_line_edit()
        self.bind('<Return>', self.adicionar_line_edit)

    def fechar_tela(self):
        self.destroy()

    def adicionar_line_edit(self, event=None):
        if len(self.entradas) >= 37:
            # Se já houver 37 entradas, não faça nada
            return

        if self.entradas:
            last_entry = self.entradas[-1]
            place_info = last_entry.place_info()
            x = place_info['relx']
            y = place_info['rely']
            nova_entrada = tk.Entry(self, width=48)
            nova_entrada.place(relx=float(x), rely=float(y) + 0.025, anchor="nw")
        else:
            nova_entrada = tk.Entry(self, width=48)
            nova_entrada.place(relx=0.001, rely=0.023, anchor="nw")
        self.entradas.append(nova_entrada)

    def get_entradas(self):
        return [entry.get() for entry in self.entradas]

class App(ctk.CTk):
     
    def __init__(self, *args, **kwargs): 
        ctk.CTk.__init__(self, *args, **kwargs)
        
        self.opened_file = ""
        self.flag_new = False 
        self.running = True
         
        self.screen_width = int(0.8 * self.winfo_screenwidth())
        self.screen_height = int(0.8 * self.winfo_screenheight())
        self.title("pFLAP")
        icon_path = "Imagens/20240322_210027.png"
        icon = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon)
        
        print("Screen size: ", self.screen_width, "x", self.screen_height)
        
        self.x = (self.screen_width // 2) - (self.screen_width//3)
        self.y = (self.screen_height // 2) - (self.screen_height//2.5)


        self.geometry(f"{self.screen_width}x{self.screen_height}+{self.x}+{self.y}")
        self.resizable(True, True)

        menu = CTkMenuBar(self)
        button_1 = menu.add_cascade("File")
        button_2 = menu.add_cascade("Test")
        button_3 = menu.add_cascade("Help")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="New (Ctrl+N)", command=lambda: self.new(self.screen_width, self.screen_height))
        dropdown1.add_option(option="Open (Ctrl+O)", command=lambda: self.open_jff())
        dropdown1.add_option(option="Save (Ctrl+S)",command=lambda: self.save())
        dropdown1.add_option(option="Save As (Ctrl+Shift+S) ",command=lambda: self.save_as_jff())

        dropdown1.add_separator()

        sub_menu = dropdown1.add_submenu("Export As")
        sub_menu.add_option(option=".PNG",command=lambda: self.export_jpg())

        dropdown2 = CustomDropdownMenu(widget=button_2)
        dropdown2.add_option(option="Multiple Run",command=lambda: self.multiple_run())
        dropdown2.add_option(option="Step by Step",command=lambda: self.Step_by_Step())

        dropdown3 = CustomDropdownMenu(widget=button_3)
        dropdown3.add_option(option="Help", command=lambda: print("Open"))
        dropdown3.add_option(option="About...",command=lambda: print("Open"))
        
        container = ctk.CTkFrame(self)  
        container.pack(side="top", fill="both", expand=True) 

        self.frames = {}  
        
        self.bind('<Key>', self.shortcut_pressed)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        for F in (StartPage,):
            frame = F(container, self)
            self.frames[F] = frame 
            frame.grid(row=0, column=0, sticky="nsew")
  
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_screen_width(self):
        return self.screen_width
    
    def set_screen_width(self, width):
        self.screen_width = width

    def get_screen_height(self):
        return self.screen_height
    
    def set_screen_height(self, height):
        self.screen_height = height

    def multiple_run(self):
        multiple_run_screen = MultipleRunScreen(self)
        entradas = multiple_run_screen.get_entradas()
        print(entradas)

    def Step_by_Step(self):
        input = ctk.CTkInputDialog(text= "Enter your test", title= "Step by step")
        input = input.get_input()
        print(input)

    def open_jff(self):
        self.filename = filedialog.askopenfilename()
        state_dict = jf.parse_xml(self.filename)
        self.opened_file = self.filename
        
        for state in state_dict:
            self.frames[StartPage].screen.index += 1
            self.frames[StartPage].screen.states.append(tela.StatesManager(int(state_dict[state]['x']), int(state_dict[state]['y']), int(state)))
  
    def save_as_jff(self):
        automaton = {}
        
        filename = filedialog.asksaveasfilename(defaultextension=".jff", filetypes=[("JFLAP files", "*.jff"), ("All files", "*.*")])
        if filename:
            for e, state in enumerate(self.frames[StartPage].screen.states):
                automaton[e] = {'name': state.state_name, 'initial': False, 'final': False, 'x': state.x, 'y': state.y}
                
            jf.write_xml(automaton, filename)
            self.opened_file = filename
  
    def save(self):
        if self.opened_file == "":
            print("Save as first")
            self.save_as_jff()
        else:
            print("Saving...")
            automaton = {}
            for e, state in enumerate(self.frames[StartPage].screen.states):
                automaton[e] = {'name': state.state_name, 'initial': False, 'final': False, 'x': state.x, 'y': state.y}
                
            jf.write_xml(automaton, self.opened_file)
  
    def new(self, screen_width, screen_height):
        self.flag_new = True
        
    def export_jpg(self):
        img = pygame.Surface((self.screen_width, self.screen_height))
        img.blit(self.frames[StartPage].screen.screen, (0, 0))
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image files", "*.png"), ("All files", "*.*")])
        pygame.image.save(img, filename)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def shortcut_pressed(self, event):
        if event.keysym == 's' and event.state & 4:  
            self.save()
        elif event.keysym == 's' and event.state & 1 and event.state & 4:
            self.save_as_jff()
        elif event.keysym == 'n' and event.state & 4:
            self.new(self.screen_width, self.screen_height)
        elif event.keysym == 'o' and event.state & 4:
            self.open_jff()
    
    def on_closing(self):
        if messagebox.askyesno("Salvar alterações", "Deseja salvar as alterações antes de fechar?"):
            self.save()
            
        pygame.quit()
        self.destroy()
        self.running = False
    
    def run(self):
        while self.running:
            if not self.flag_new:
                self.frames[StartPage].screen.running()
            else:
                pygame.quit()
                self.frames[StartPage].screen = tela.Screen(self.screen_width, self.screen_height)
                self.flag_new = False
                
            self.update()
    
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        screen_width = 40
        screen_height = 691

        self.label_side_bar = ctk.CTkLabel(self, width=screen_width, height=screen_height, text="")
        self.label_side_bar.grid(row=0, column=0)
        
        self.pygamelabel = tk.Label(self, width=int(controller.screen_width*2), height=int(controller.screen_height*0.07), text="")
        os.environ['SDL_WINDOWID'] = str(self.pygamelabel.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.pygamelabel.grid(row=0, column=1, columnspan=3, padx=10, sticky="nsew")
        self.screen = tela.Screen(screen_width, screen_height)
        
        button_width = 20
        button_height = 20

        self.label_txt = ctk.CTkLabel(self.label_side_bar, text="Editor", height= button_height, width= button_width, font=("Helvetica", 12),anchor="e")
        self.label_txt.place(relx=0.1, rely=0.05, anchor="w")

        icon_edition = tk.PhotoImage(file="Imagens/20240322_203742.png")
        icon_edition = icon_edition.subsample(2, 2)
        self.Button_attribute_edition = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_edition, compound="right")
        self.Button_attribute_edition.place(relx=0.03, rely=0.13, anchor="w")
        
        icon_state_creator = tk.PhotoImage(file="Imagens/20240322_210027.png")
        icon_state_creator = icon_state_creator.subsample(2, 2)
        self.Button_state_creator = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_state_creator, compound="right")
        self.Button_state_creator.place(relx=0, rely=0.23, anchor="w")
        
        icon_transition_creator = tk.PhotoImage(file="Imagens/20240322_210202.png")
        icon_transition_creator = icon_transition_creator.subsample(2, 2)
        self.Button_transition_creator = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_transition_creator, compound="right")
        self.Button_transition_creator.place(relx=0, rely=0.33, anchor="w")
        
        icon_deleter = tk.PhotoImage(file="Imagens/20240322_193952.png")
        imagem_reduzida = icon_deleter.subsample(2, 2)
        self.Button_deleter = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, fg_color="transparent", 
                                            image=imagem_reduzida, compound="left")
        self.Button_deleter.place(relx=0.03, rely=0.43, anchor="w")
        
        icon_undoer = tk.PhotoImage(file="Imagens/20240322_210234.png")
        icon_undoer = icon_undoer.subsample(2, 2)
        self.Button_undoer = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_undoer, compound="right")
        self.Button_undoer.place(relx=0, rely=0.53, anchor="w")
        
        
        icon_remake = tk.PhotoImage(file="Imagens/20240322_211523.png")
        icon_remake = icon_remake.subsample(2, 2)
        self.Button_remake = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_remake, compound="right")
        self.Button_remake.place(relx=0, rely=0.63, anchor="w")

app = App()
app.run()