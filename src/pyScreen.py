import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import pyGameGenericFSM as p
import os
import pygame

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
        
        container = ctk.CTkFrame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}  
  
        for F in (StartPage, PageOne, PageTwo):
  
            frame = F(container, self)
  
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
  
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def run(self):
        while True:
            pygame.display.update()
            self.frames[StartPage].space.current_state()
            self.update()
        
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Start Page", font = LARGEFONT)
        label.grid(row = 0, column = 1, columnspan = 2)
        
        self.rowconfigure(0, weight = 2)
        self.columnconfigure(2, weight = 2)
  
        button = ctk.CTkButton(self, text ="Go to Page 1", command = lambda : controller.show_frame(PageOne))
  
        button.grid(row = 1, column = 1, padx = 10, sticky = "e")
  
        button2 = ctk.CTkButton(self, text ="Go to Page 2", command= lambda : controller.show_frame(PageTwo))
  
        button2.grid(row=1, column = 2, padx = 10, sticky = "e")
        
        self.pygamelabel = tk.Label(self, width=120, height=35, text="")
        os.environ['SDL_WINDOWID'] = str(self.pygamelabel.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        
        self.pygamelabel.grid(row=2, column=1, columnspan=2)
        self.space = p.Space(720, 480)

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