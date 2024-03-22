import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import pyGameGenericFSM as p
from customtkinter import filedialog
import os
import pygame
import tela
import JFLAPimport as jf

LARGEFONT =("Verdana", 35)

class App(ctk.CTk):
     
    def __init__(self, *args, **kwargs): 
        ctk.CTk.__init__(self, *args, **kwargs)
        pygame.init()
         
        self.screen_width = int(0.8 * self.winfo_screenwidth())
        self.screen_height = int(0.8 * self.winfo_screenheight())
        
        print("Screen size: ", self.screen_width, "x", self.screen_height)
        
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.resizable(False, False)
        
        self.filename = ""
        
        container = ctk.CTkFrame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}  
  
        for F in (StartPage, PageOne, PageTwo):
  
            frame = F(container, self)
  
            self.frames[F] = frame 
  
            frame.pack()
  
        self.show_frame(StartPage)
    
    def import_jff(self):
        self.filename = filedialog.askopenfilename()
        state_dict = jf.parse_xml(self.filename)
        
        for state in state_dict:
            self.frames[StartPage].screen.index += 1
            self.frames[StartPage].screen.states.append(tela.StatesManager(int(state_dict[state]['x']), int(state_dict[state]['y']), int(state)))
  
    def export_jff(self):
        automaton = {}
        
        for e, state in enumerate(self.frames[StartPage].screen.states):
            automaton[e] = {'name': state.state_name, 'initial': False, 'final': False, 'x': state.x, 'y': state.y}
           
        jf.write_xml(automaton, 'test.jff')
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def run(self):
        while True:
            self.frames[StartPage].screen.running()
            self.update()
        
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Start Page", font = LARGEFONT)
        label.grid(row = 0, column = 1, columnspan = 2)
        
        # Configure row weights for better layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=4)
        
        # Configure column weights for better layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Add more buttons
        button1 = ctk.CTkButton(self, text="Importar arquivo", command=lambda: controller.import_jff())
        button1.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        button2 = ctk.CTkButton(self, text="Exportar arquivo", command=lambda: controller.export_jff())
        button2.grid(row=1, column=1, padx=10, pady=5)

        button3 = ctk.CTkButton(self, text="New Button 3", command=lambda: print("Button 3 clicked"))
        button3.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        # Reposition existing buttons
        button1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        button2.grid(row=1, column=1, padx=10, pady=5)
        button3.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        # Reposition the pygame label
        self.pygamelabel = tk.Label(self, width=int(controller.screen_width*2), height=int(controller.screen_height*0.07), text="")
        os.environ['SDL_WINDOWID'] = str(self.pygamelabel.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.pygamelabel.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.screen = tela.Screen(720, 480)


class PageOne(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Page One", font = LARGEFONT)
        label.pack(pady = 10, padx = 10)
  
        button = ctk.CTkButton(self, text ="Go to Page 1", command = lambda : controller.show_frame(PageOne))
        button.pack()
  
        button2 = ctk.CTkButton(self, text ="Go to Page 2", command= lambda : controller.show_frame(PageTwo))
        button2.pack()
        
class PageTwo(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Page Two", font = LARGEFONT)
        label.pack(pady = 10, padx = 10)
        
        button = ctk.CTkButton(self, text ="Go to Page 1", command = lambda : controller.show_frame(StartPage))
        
        button.pack()
        
        button2 = ctk.CTkButton(self, text ="Go to Page 2", command= lambda : controller.show_frame(PageTwo))
        
        button2.pack()

app = App()
app.run()