import tkinter as tk
import customtkinter as ctk
from CTkMenuBar import *

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        screen_width = 50
        screen_height = 691

        self.label_side_bar = ctk.CTkLabel(self, width=screen_width, height=screen_height)
        self.label_side_bar.grid(row=0, column=1, sticky="nsew")
        
        self.container_buttons = ctk.CTkFrame(self.label_side_bar, width=screen_width, height=screen_height)
        self.container_buttons.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)  # Para preencher a largura da janela
        self.grid_columnconfigure(0, weight=1)  # Para pree

        button_width = 2
        button_height = 10

        self.Button_attribute_edition = ctk.CTkButton(self.container_buttons, width=10, height=button_height)
        self.Button_attribute_edition.place(relx=0, rely=0.13, anchor="w")
        
        self.Button_state_creator = ctk.CTkButton(self.container_buttons, width=button_width, height=button_height)
        self.Button_state_creator.place(relx=0, rely=0.20, anchor="w")
        
        self.Button_transition_creator = ctk.CTkButton(self.container_buttons, width=button_width, height=button_height)
        self.Button_transition_creator.place(relx=0, rely=0.27, anchor="w")
        
        self.Button_deleter = ctk.CTkButton(self.container_buttons, width=button_width, height=button_height)
        self.Button_deleter.place(relx=0, rely=0.34, anchor="w")
        
        self.Button_undoer = ctk.CTkButton(self.container_buttons, width=button_width, height=button_height)
        self.Button_undoer.place(relx=0, rely=0.41, anchor="w")
        
        self.Button_remake = ctk.CTkButton(self.container_buttons, width=button_width, height=button_height)
        self.Button_remake.place(relx=0, rely=0.48, anchor="w")

class App(ctk.CTk):
     
    def __init__(self, *args, **kwargs): 
        ctk.CTk.__init__(self, *args, **kwargs)
         
        self.screen_width = int(0.8 * self.winfo_screenwidth())
        self.screen_height = int(0.8 * self.winfo_screenheight())
        
        print("Screen size: ", self.screen_width, "x", self.screen_height)
        
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.resizable(True, True)
        
        self.filename = ""

        menu = CTkMenuBar(self)
        button_1 = menu.add_cascade("File")
        button_2 = menu.add_cascade("Edit")
        button_3 = menu.add_cascade("Settings")
        button_4 = menu.add_cascade("About")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="Open", command=lambda: print("Open"))
        dropdown1.add_option(option="Save",command=lambda: print("Open"))

        dropdown1.add_separator()

        sub_menu = dropdown1.add_submenu("Export As",command=lambda: print("Open"))
        sub_menu.add_option(option=".TXT",command=lambda: print("Open"))
        sub_menu.add_option(option=".PDF",command=lambda: print("Open"))

        dropdown2 = CustomDropdownMenu(widget=button_2)
        dropdown2.add_option(option="Cut",command=lambda: print("Open"))
        dropdown2.add_option(option="Copy",command=lambda: print("Open"))
        dropdown2.add_option(option="Paste",command=lambda: print("Open"))

        dropdown3 = CustomDropdownMenu(widget=button_3)
        dropdown3.add_option(option="Preferences",command=lambda: print("Open"))
        dropdown3.add_option(option="Update",command=lambda: print("Open"))

        dropdown4 = CustomDropdownMenu(widget=button_4)
        dropdown4.add_option(option="Hello World",command=lambda: print("Open"))
        
        container = ctk.CTkFrame(self)  
        container.pack(side="top", fill="both", expand=True) 

        self.frames = {}  

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

    

app = App()
app.mainloop()
