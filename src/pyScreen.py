import pygame
import sys
from src.StatesManager import StatesManager
import tkinter as tk
from tkinter import simpledialog
import math
import sys
import os

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    else:
        return relative_path

def distance_by_point(x1, y1, x2, y2, x, y, distancia_maxima=6):
    distancia = abs((y2-y1)*x - (x2-x1)*y + x2*y1 - y2*x1) / math.sqrt((y2-y1)**2 + (x2-x1)**2)

    return distancia <= distancia_maxima

def make_message_box():
    root = tk.Tk()
    root.withdraw()

    texto = simpledialog.askstring("Digite um simbolo", "Digite seu simbolo aqui:")

    if texto is not None:
        return texto
    else:
        return None

class Screen():
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.var_inicial = tk.BooleanVar()
        self.var_final = tk.BooleanVar()
        
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        pygame.display.set_caption("pFlap")

        font = pygame.font.Font(None, 30)
        self.origin_state : StatesManager = None
        self.destination_state : StatesManager = None
        self.flag = "0"
        self.current_select_state = None
        self.initial_state = None
        self.final_states = []
        self.states = []
        self.error_sound = pygame.mixer.Sound(resource_path("src/assets/snd_error.wav"))
        self.index = 0
        self.action = "Criar Estado"
        
    def running(self):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Botão direito do mouse
                if self.action == "Selecionar":
                    print("Properties")
                    self.properties()

                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
                x, y = pygame.mouse.get_pos()
                # cria novos estados
                if self.action == "Criar Estado":
                    can_create_circle = True
                    for state in self.states:
                        if state.is_too_close(StatesManager(x, y, self.index)):
                            can_create_circle = False
                            self.error_sound.play() 
                            break
                    if can_create_circle:
                        self.states.append(StatesManager(x, y, self.index))
                        self.index += 1
                elif self.action == "Selecionar":
                    self.select_state()
                
                elif self.action == "Criar Transição":
                    self.make_transition()
                    pass
                        
                # deleta estados já existentes
                elif self.action == "Excluir Estado":
                    self.remove()

        self.screen.fill((255, 255, 255))
        
        if self.current_select_state != None:
            self.current_select_state.x = mouse_x
            self.current_select_state.y = mouse_y    
    
        if self.action== "Excluir Estado":
            fonte = pygame.font.Font(None, 30)
            x = fonte.render("X", True, (255, 0, 0))
            self.screen.blit(x, (mouse_x + 12, mouse_y - 12))
            
        if self.action== "Criar Estado":
            fonte = pygame.font.Font(None, 50)
            x = fonte.render("+", True, (0, 0, 255))
            self.screen.blit(x, (mouse_x + 12, mouse_y - 12))
            
        if self.action== "Criar Transição":
            fonte = pygame.font.Font(None, 30)
            x = fonte.render("->", True, (0, 0, 255))
            self.screen.blit(x, (mouse_x + 12, mouse_y - 12))
            
            if self.flag == "1":
                pygame.draw.line(self.screen, (0, 0, 0), (self.origin_state.x, self.origin_state.y), (mouse_x, mouse_y), 5)
            
        for state in self.states:
            state.draw(self.screen)
        
        pygame.display.flip()
    
    def properties(self):
        x, y = pygame.mouse.get_pos()
        for state in self.states:
            if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                self.select_popup()
                self.destination_state = state
    
    def set_initial(self):
        if self.destination_state.initial:
            self.destination_state.initial = False
            self.initial_state = None
        else:
            self.destination_state.initial = True
            self.initial_state = self.destination_state
        self.destination_state = None
        self.poup.destroy()
    
    def set_final(self):
        if self.destination_state.final:
            self.destination_state.final = False
            self.final_states.remove(self.destination_state.state_name)
        else:
            self.destination_state.final = True
            self.final_states.append(self.destination_state.state_name)
        self.destination_state = None
        self.poup.destroy()
        
    def select_popup(self):
        x, y = pygame.mouse.get_pos()
        print(x, y)
        if self.destination_state == None:
            self.poup = tk.Tk()
            self.poup.geometry(f"+{x+250}+{y+150}")
            self.poup.title("Properties")
            self.poup.overrideredirect(True)
            set_initial = tk.Button(self.poup, text="Set/Unset Initial", command=self.set_initial)
            set_initial.grid(row=0, column=0, sticky="nsew")
            set_final = tk.Button(self.poup, text="Set/Unset Final", command=self.set_final)
            set_final.grid(row=1, column=0, sticky="nsew")
        
    def remove(self):
        x, y = pygame.mouse.get_pos()
        for state in self.states:
            if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                self.states.remove(state)
            
            for transition in state.transition_list:
                if distance_by_point(x, y, state.x, state.y, transition[0].x, transition[0].y):
                    state.transition_list.remove(transition)
                    
    def make_transition(self):
        x, y = pygame.mouse.get_pos()
        for state in self.states:
            if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                if self.flag == "0":
                    print(state)
                    self.origin_state = state
                    self.flag = "1"
                elif self.flag == "1":
                    symbol = make_message_box()
                    self.destination_state = state
                    self.origin_state.add_transition(self.destination_state, symbol)
                    self.origin_state = None
                    self.destination_state = None
                    self.flag = "0"
                    
    def select_state(self):
        if self.current_select_state == None:
            x, y = pygame.mouse.get_pos()
            for state in self.states:
                if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                        self.current_select_state = state
        else:
            print(self.current_select_state.transition_list)
            self.current_select_state = None
            
    def zoom_in(self):
        for state in self.states:
            state.zoom(1.1)
            
    def load(self, states):
        
        for state in states:
            self.states.append(state)
        
            if state.initial:
                self.initial_state = state
            if state.final:
                self.final_states.append(state.state_name)