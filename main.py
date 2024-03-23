from tkinter import *
import customtkinter as ctk
from CTkMenuBar import *

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        screen_width = 40
        screen_height = 691

        self.label_side_bar = ctk.CTkLabel(self, width=screen_width, height=screen_height, text="")
        self.label_side_bar.grid(row=0, column=0)

        button_width = 20
        button_height = 20

        self.label_txt = ctk.CTkLabel(self.label_side_bar, text="Editor", height= button_height, width= button_width, font=("Helvetica", 12),anchor="e")
        self.label_txt.place(relx=0.1, rely=0.05, anchor="w")

        icon_edition = PhotoImage(file="Imagens/20240322_203742.png")
        icon_edition = icon_edition.subsample(2, 2)
        self.Button_attribute_edition = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_edition, compound="right")
        self.Button_attribute_edition.place(relx=0.03, rely=0.13, anchor="w")
        
        icon_state_creator = PhotoImage(file="Imagens/20240322_210027.png")
        icon_state_creator = icon_state_creator.subsample(2, 2)
        self.Button_state_creator = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_state_creator, compound="right")
        self.Button_state_creator.place(relx=0, rely=0.23, anchor="w")
        
        icon_transition_creator = PhotoImage(file="Imagens/20240322_210202.png")
        icon_transition_creator = icon_transition_creator.subsample(2, 2)
        self.Button_transition_creator = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_transition_creator, compound="right")
        self.Button_transition_creator.place(relx=0, rely=0.33, anchor="w")
        
        icon_deleter = PhotoImage(file="Imagens/20240322_193952.png")
        imagem_reduzida = icon_deleter.subsample(2, 2)
        self.Button_deleter = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, fg_color="transparent", 
                                            image=imagem_reduzida, compound="left")
        self.Button_deleter.place(relx=0.03, rely=0.43, anchor="w")
        
        icon_undoer = PhotoImage(file="Imagens/20240322_210234.png")
        icon_undoer = icon_undoer.subsample(2, 2)
        self.Button_undoer = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_undoer, compound="right")
        self.Button_undoer.place(relx=0, rely=0.53, anchor="w")
        
        
        icon_remake = PhotoImage(file="Imagens/20240322_211523.png")
        icon_remake = icon_remake.subsample(2, 2)
        self.Button_remake = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_remake, compound="right")
        self.Button_remake.place(relx=0, rely=0.63, anchor="w")


class App(ctk.CTk):
     
    def __init__(self, *args, **kwargs): 
        ctk.CTk.__init__(self, *args, **kwargs)
         
        self.screen_width = int(0.8 * self.winfo_screenwidth())
        self.screen_height = int(0.8 * self.winfo_screenheight())
        self.title("pFLAP")
        icon_path = "Imagens/20240322_210027.png"
        icon = PhotoImage(file=icon_path)
        self.iconphoto(True, icon)
        
        print("Screen size: ", self.screen_width, "x", self.screen_height)
        
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.resizable(True, True)

        menu = CTkMenuBar(self)
        button_1 = menu.add_cascade("File")
        button_2 = menu.add_cascade("Test")
        button_3 = menu.add_cascade("Help")

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
