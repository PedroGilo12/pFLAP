import pygame
import sys
from ButtonBar import ButtonBar
from StatesManager import StatesManager
import tkinter as tk
from tkinter import simpledialog
import math

def ponto_proximo_linha(x1, y1, x2, y2, x, y, distancia_maxima=6):
    distancia = abs((y2-y1)*x - (x2-x1)*y + x2*y1 - y2*x1) / math.sqrt((y2-y1)**2 + (x2-x1)**2)

    return distancia <= distancia_maxima

def make_message_box():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    texto = simpledialog.askstring("Digite um simbolo", "Digite seu simbolo aqui:")

    if texto is not None:
        return texto
    else:
        return None

class Screen():
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        pygame.display.set_caption("pFlap")

        font = pygame.font.Font(None, 30)
        self.origin_state : StatesManager = None
        self.destination_state : StatesManager = None
        self.flag = "0"
        self.current_select_state = None

        self.button_definitions = [
            {'position': (50, 10), 'size': (200, 50), 'color': (0, 0, 255), 'text': "Criar Estado"},
            {'position': (300, 10), 'size': (200, 50), 'color': (255, 0, 0), 'text': "Excluir Estado"}
        ]

        self.button_bar = ButtonBar(self.screen, font, self.button_definitions)

        self.states = []
        self.error_sound = pygame.mixer.Sound("src/assets/snd_error.wav")
        self.index = 0
        self.action = "Criar Estado"
        
    def running(self):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Botão direito do mouse
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
                x, y = pygame.mouse.get_pos()
                if self.button_bar.button_area_rect.collidepoint(x, y):
                    for rect, _, _ in self.button_bar.buttons:
                        if rect.collidepoint(x, y):
                            # Altera o valor de self.action com base no texto do botão clicado
                            for button_definition in self.button_definitions:
                                if button_definition['position'] == rect.topleft:
                                    print(button_definition['text'])
                                    self.action = button_definition['text']
                                    break
                            break
                # cria novos estados
                elif self.action == "Criar Estado" and y - 50 > self.button_definitions[1]['position'][1] + 50:
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
        
    def remove(self):
        x, y = pygame.mouse.get_pos()
        for state in self.states:
            if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                self.states.remove(state)
            
            for transition in state.transition_list:
                if ponto_proximo_linha(x, y, state.x, state.y, transition[0].x, transition[0].y):
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