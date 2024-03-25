import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from customtkinter import filedialog
import os
import pygame
from CTkMenuBar import *
import CTkListbox as clb
from tkinter import messagebox
import sys

import src.StateMachine as sm
import src.StatesManager as smgr
import src.pyScreen as pyScreen
import src.JFLAPimport as jf

LARGEFONT =("Verdana", 35)

ctk.set_appearance_mode("dark")

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    else:
        return relative_path

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack(ipadx=2)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()

class MultipleRunScreen(tk.Toplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent

        self.controller = controller
        self.overrideredirect(True)
        self.geometry("600x828+1149+143")
        self.configure(bg="#333333")

        self.input_label = tk.Label(self, text="Input", bg="#C0C0C0", fg="black", width=53, borderwidth=1, relief="solid")
        self.input_label.place(relx=0.2, rely=0, anchor="n")

        self.output_label = tk.Label(self, text="Output", bg="#C0C0C0", fg="black", width=53, borderwidth=1, relief="solid")
        self.output_label.place(relx=0.8, rely=0, anchor="n")
        
        self.close_button = tk.Button(self, text="X", bg="red", fg="white", command=self.close_window)
        self.close_button.place(relx=1, rely=0.012, anchor="e")

        self.run_button = tk.Button(self, text="Run", bg="#696969", fg="white", command=self.show_results, width=20, font= ("Verdana", 12))
        self.run_button.place(relx=0.5, rely=0.995, anchor="s")

        self.inputs = []
        self.result_labels = []

        self.add_entry()
        self.bind('<Return>', self.add_entry)

    def close_window(self):
        self.destroy()

    def add_entry(self, event=None):
        if len(self.inputs) >= 37:
            return

        if self.inputs:
            last_entry = self.inputs[-1]
            place_info = last_entry.place_info()
            x = place_info['relx']
            y = place_info['rely']
            new_entry = tk.Entry(self, width=48)
            new_entry.place(relx=float(x), rely=float(y) + 0.025, anchor="nw")

            result_label = tk.Label(self, width=43,  bg="white", height=0, relief="solid", highlightthickness=0, highlightbackground="gray")
            result_label.place(relx=0.49, rely=(float(y)-0.001) + 0.025, anchor="nw")
        else:
            new_entry = tk.Entry(self, width=48)
            new_entry.place(relx=0.001, rely=0.024, anchor="nw")
            
            result_label = tk.Label(self, width=43, bg="white", height=0, relief="solid", highlightthickness=0)
            result_label.place(relx=0.49, rely=0.023, anchor="nw")
        self.inputs.append(new_entry)
        self.result_labels.append(result_label)
        
    def show_results(self):
        results = self.get_entries()
        print(results)
        
        self.controller.inputs = results
        self.controller.simulation()

    def get_entries(self):
        return [entry.get() for entry in self.inputs]

class App(ctk.CTk):
     
    def __init__(self, *args, **kwargs): 
        ctk.CTk.__init__(self, *args, **kwargs)
        
        self.opened_file = ""
        self.flag_new = False 
        self.running = True
        self.inputs = []
         
        self.screen_width = int(0.8 * self.winfo_screenwidth())
        self.screen_height = int(0.8 * self.winfo_screenheight())
        self.title("pFLAP")
        icon_path = resource_path("src/assets/img/20240322_210027.png")
        icon = tk.PhotoImage(file=icon_path)
        self.iconphoto(True, icon)
        
        print("Screen size: ", self.screen_width, "x", self.screen_height)
        
        self.x = (self.screen_width // 2) - (self.screen_width//3)
        self.y = (self.screen_height // 2) - (self.screen_height//2.5)


        self.geometry(f"{self.screen_width}x{self.screen_height}+{self.x}+{self.y}")
        self.resizable(False, False)

        menu = CTkMenuBar(self)
        button_1 = menu.add_cascade("File")
        button_2 = menu.add_cascade("Test")
        button_3 = menu.add_cascade("Help")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="New (Ctrl+N)", command=lambda: self.new(self.screen_width, self.screen_height))
        dropdown1.add_option(option="Open (Ctrl+O)", command=lambda: self.open_jff())
        dropdown1.add_option(option="Save (Ctrl+S)",command=lambda: self.save())
        dropdown1.add_option(option="Save As (Ctrl+A) ",command=lambda: self.save_as_jff())

        dropdown1.add_separator()

        sub_menu = dropdown1.add_submenu("Export As")
        sub_menu.add_option(option=".PNG",command=lambda: self.export_jpg())

        dropdown2 = CustomDropdownMenu(widget=button_2)
        dropdown2.add_option(option="Multiple Run",command=lambda: self.multiple_run())
        dropdown2.add_option(option="Step by Step",command=lambda: self.simulation(True))

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
        self.multiple_run_screen = MultipleRunScreen(self, controller=self)
        entradas = self.multiple_run_screen.get_entries()
        print(entradas)

    def open_jff(self):
        self.filename = filedialog.askopenfilename()
        state_dict = jf.parse_xml(self.filename)
        self.opened_file = self.filename
        self.frames[StartPage].screen.load(state_dict)
    
    def Step_by_Step(self):
        input = ctk.CTkInputDialog(text= "Enter your test", title= "Step by step")
        input = input.get_input()
        return input

    def convert_jff_to_fsm(self, jff: list[smgr.StatesManager]):
        fsm: dict[str, sm.State] = {}
        
        for state in jff:
            transition_list = []
            for transition in state.transition_list:
                transition_list.append(tuple((state.state_name, transition[1], transition[0].state_name)))
            
            fsm[state.state_name] = sm.State(state.state_name, transition_list)
        
            print(f"{fsm[state.state_name].name}: {fsm[state.state_name].elements}")
        
        return fsm
            
    def simulation(self, step: bool = False):
        
        states = self.convert_jff_to_fsm(self.frames[StartPage].screen.states)
        
        if self.frames[StartPage].screen.initial_state == None:
            messagebox.showerror(title="Error", message="Initial state not defined")
            return
        
        initial = self.frames[StartPage].screen.initial_state.state_name
        final_states = self.frames[StartPage].screen.final_states
        print(f"inicial: {initial}")
        print(f"estados finais: {final_states}")
        
        if initial == "" or final_states == []:
            messagebox.showerror(title="Error", message="Initial state or final states not defined")
            return
        
        if not step:

            for e, input in enumerate(self.inputs):
                self.machine = sm.FiniteStateMachine(states, states[initial], final_states)
                
                for signal in list(input):
                    self.machine.process_symbol(signal)
                    
                print(self.machine.result())
                if any(self.machine.result()):
                    self.multiple_run_screen.result_labels[e].configure(text="Accepted")
                else:
                    self.multiple_run_screen.result_labels[e].configure(text="Rejected")  
            
        else:
            self.machine = sm.FiniteStateMachine(states, states[initial], final_states)
            input = self.Step_by_Step()
            if input != "":
                signals = list(input)
                self.frames[StartPage].step_by_step(signals)
            
                    
    def save_as_jff(self):
        automaton = {}
        
        filename = filedialog.asksaveasfilename(defaultextension=".jff", filetypes=[("JFLAP files", "*.jff"), ("All files", "*.*")])
        if filename:
            jf.write_xml(self.frames[StartPage].screen.states, filename)
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
        elif event.keysym == 'a' and event.state & 4:
            self.save_as_jff()
        elif event.keysym == 'n' and event.state & 4:
            self.new(self.screen_width, self.screen_height)
        elif event.keysym == 'o' and event.state & 4:
            self.open_jff()
        elif event.keysym == 'e' and event.state & 4:
            self.frames[StartPage].select()
        elif event.keysym == 'm' and event.state & 4:
            self.frames[StartPage].add_option()
        elif event.keysym == 't' and event.state & 4:
            self.frames[StartPage].make_transition()
        elif event.keysym == 'd' and event.state & 4:
            self.frames[StartPage].remove_option()
            
            
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
                self.frames[StartPage].screen = pyScreen.Screen(self.screen_width, self.screen_height)
                self.flag_new = False
                
            self.update()

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        self.simulation_index = 0
        
        screen_width = 40
        screen_height = 691
        
        self.controller = controller

        self.label_side_bar = ctk.CTkLabel(self, width=screen_width, height=screen_height, text="")
        self.label_side_bar.grid(row=0, column=0)
        
        self.pygamelabel = tk.Label(self, width=int(controller.screen_width*2), height=int(controller.screen_height*0.07), text="")
        os.environ['SDL_WINDOWID'] = str(self.pygamelabel.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        self.pygamelabel.grid(row=0, column=1, columnspan=3, padx=10, sticky="nsew")
        self.screen = pyScreen.Screen(screen_width, screen_height)
        
        button_width = 20
        button_height = 20

        self.label_txt = ctk.CTkLabel(self.label_side_bar, text="Editor", height= button_height, width= button_width, font=("Helvetica", 12),anchor="e")
        self.label_txt.place(relx=0.1, rely=0.05, anchor="w")

        icon_edition = tk.PhotoImage(file=resource_path("src/assets/img/20240322_203742.png"))
        icon_edition = icon_edition.subsample(2, 2)
        self.Button_attribute_edition = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_edition, compound="right", command=self.select)
        self.Button_attribute_edition.place(relx=0.03, rely=0.13, anchor="w")
        
        icon_state_creator = tk.PhotoImage(file=resource_path("src/assets/img/20240322_210027.png"))
        icon_state_creator = icon_state_creator.subsample(2, 2)
        self.Button_state_creator = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_state_creator, compound="right", command= self.add_option)
        self.Button_state_creator.place(relx=0, rely=0.23, anchor="w")
        
        icon_transition_creator = tk.PhotoImage(file=resource_path("src/assets/img/20240322_210202.png"))
        icon_transition_creator = icon_transition_creator.subsample(2, 2)
        self.Button_transition_creator = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, 
                                                      fg_color="transparent", image=icon_transition_creator, compound="right", command=self.make_transition)
        self.Button_transition_creator.place(relx=0, rely=0.33, anchor="w")
        
        icon_deleter = tk.PhotoImage(file=resource_path("src/assets/img/20240322_193952.png"))
        imagem_reduzida = icon_deleter.subsample(2, 2)
        self.Button_deleter = ctk.CTkButton(self.label_side_bar, text="", height= button_height, width= button_width, fg_color="transparent", 
                                            image=imagem_reduzida, compound="left", command=self.remove_option)
        self.Button_deleter.place(relx=0.03, rely=0.43, anchor="w")
        
        #Cria ToolTips:
        ToolTip(self.Button_attribute_edition, text="Edit attributes (Ctrl + E)")
        ToolTip(self.Button_state_creator, text="Create state (Ctrl + M)")
        ToolTip(self.Button_transition_creator, text="Create transition (Ctrl + T)")
        ToolTip(self.Button_deleter, text="Delete (Ctrl + D)")
        
        self.step_listt = {}
        
    def remove_option(self):
        self.screen.action = "Excluir Estado"
    
    def add_option(self):
        self.screen.action = "Criar Estado"
        
    def make_transition(self):
        self.screen.action = "Criar Transição"
        
    def select(self):
        self.screen.action = "Selecionar"
    
    def step_by_step(self, symbols: list):
        
        self.step_listt = {}
        self.simulation_index = 0
        sbs_screen = ctk.CTkToplevel(self)
        sbs_screen.title("Step by step")
        sbs_screen.geometry("{}x{}".format(int(self.controller.screen_width * 0.6), int(self.controller.screen_height * 0.3)))
        
        sbs_screen.resizable(False, False)
        sbs_screen.rowconfigure(0, weight=2)
        
        self.previous_step_label = ctk.CTkLabel(sbs_screen, text=f"", width=int(self.controller.screen_width * 0.21), height=int(self.controller.screen_height/2))
        self.previous_step_label.grid(row=0, column=1, padx=self.controller.screen_width * 0.00555, pady=self.controller.screen_height * 0.00555, sticky="nsew")
        
        self.current_step_label = ctk.CTkLabel(sbs_screen, text=f"Current State : {self.controller.machine.get_state()}", width=int(self.controller.screen_width* 0.21), height=int(self.controller.screen_height/3), bg_color="green", corner_radius=0.1)
        self.current_step_label.grid(row=0, column=2, padx=self.controller.screen_width * 0.00555, pady=self.controller.screen_height * 0.00555, sticky="nsew")
        
        self.step_list = clb.CTkListbox(sbs_screen, command= self.update_step)
        self.step_list.grid(row=0, column=0, padx=self.controller.screen_width * 0.00555, sticky="nsew")
        
        button = ctk.CTkButton(sbs_screen, text="Next", command=self.add_step)
        button.grid(row=1, column=0, padx=self.controller.screen_width * 0.00555, sticky="nsew", columnspan=3)
        
        self.text_by_symbol = "".join(symbols)
        
        self.input_label = ctk.CTkLabel(sbs_screen, text=self.text_by_symbol, anchor = "center")
        self.input_label.grid(row=2, padx=self.controller.screen_width * 0.00555, sticky="nsew", columnspan=3)

    def add_step(self):
        if self.simulation_index < len(self.text_by_symbol):
            previous_state = self.controller.machine.get_state()
            
            self.controller.machine.process_symbol(self.text_by_symbol[self.simulation_index])
            current_state = self.controller.machine.get_state()
            
            self.step_listt[f"Step {self.simulation_index}"] = [previous_state, current_state, self.simulation_index]
            self.step_list.insert("end", f"Step {self.simulation_index}")
            self.update_step(f"Step {self.simulation_index}")
            self.simulation_index = self.simulation_index + 1
    
    def update_step(self, text):
        att_list = self.step_listt[text]
        if att_list[1] == "undefined":
            self.current_step_label.configure(bg_color="red")
        else:
            self.current_step_label.configure(bg_color="green")
            
        if att_list[0] == "undefined":
            self.previous_step_label.configure(bg_color="red")
        else:
            self.previous_step_label.configure(bg_color="gray")
            
        self.current_step_label.configure(text=f"Current State : {att_list[1]}")
        self.previous_step_label.configure(text=f"Previous State : {att_list[0]}")
        self.paint_char(self.input_label, att_list[2])
    
    def paint_char(self, label, indice_n):
        texto = self.text_by_symbol
        novo_texto = texto[:indice_n] + f'>{texto[indice_n]}<' + texto[indice_n+1:]
        label.configure(text=novo_texto)