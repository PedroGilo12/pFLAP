from tkinter import simpledialog
import pygame
from ButtonBar import ButtonBar
from StatesManager import StatesManager
import math
import tkinter as tk

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

class Screen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        pygame.init()
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        pygame.display.set_caption("pFlap")

        self.states = []
        self.error_sound = pygame.mixer.Sound("src/assets/snd_error.wav")
        self.action = "Create Transition"
        self.index = 0

        self.font = pygame.font.Font(None, 30)
        self.origin_state : StatesManager = None
        self.destination_state : StatesManager = None
        self.flag = "0"
        self.current_select_state = None

        self.button_definitions = [
        {'position': (50, 10), 'size': (200, 50), 'color': (0, 0, 255), 'text': "Create State"},
        {'position': (300, 10), 'size': (200, 50), 'color': (255, 0, 0), 'text': "Delete State"},
        {'position': (550, 10), 'size': (200, 50), 'color': (0, 255, 0), 'text': "Create Transition"}
        ]

        self.button_bar = ButtonBar(self.surface, self.font, self.button_definitions)

    def running(self):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Botão direito do mouse
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
                if self.button_bar.button_area_rect.collidepoint(mouse_x, mouse_y):
                    for rect, _, _ in self.button_bar.buttons:
                        if rect.collidepoint(mouse_x, mouse_y):
                            # Altera o valor de self.action com base no texto do botão clicado
                            for button_definition in self.button_definitions:
                                if button_definition['position'] == rect.topleft:
                                    print(button_definition['text'])
                                    self.action = button_definition['text']
                                    break
                            break
                # cria novos estados
                elif self.action == "Create State" and mouse_y - 50 > self.button_definitions[1]['position'][1] + 50:
                    self.create_state()

                # seleciona estados existentes
                elif self.action == "Selecionar":
                    self.select_state()
                
                elif self.action == "Create Transition":
                    self.make_transition()
                        
                # deleta estados já existentes
                elif self.action == "Delete State":
                    self.delete_state()

        self.surface.fill((255, 255, 255))
        self.button_bar.draw()
        
        if self.current_select_state != None:
            self.current_select_state.x = mouse_x
            self.current_select_state.y = mouse_y    
    
        if self.action== "Delete State":
            fonte = pygame.font.Font(None, 30)
            x = fonte.render("X", True, (255, 0, 0))
            self.surface.blit(x, (mouse_x + 12, mouse_y - 12))
            
        if self.action== "Create State":
            fonte = pygame.font.Font(None, 50)
            x = fonte.render("+", True, (0, 0, 255))
            self.surface.blit(x, (mouse_x + 12, mouse_y - 12))
            
        if self.action== "Create Transition":
            fonte = pygame.font.Font(None, 30)
            x = fonte.render("->", True, (0, 0, 255))
            self.surface.blit(x, (mouse_x + 12, mouse_y - 12))
            
            if self.flag == "1":
                pygame.draw.line(self.surface, (0, 0, 0), (self.origin_state.x, self.origin_state.y), (mouse_x, mouse_y), 5)
            
        for state in self.states:
            state.draw(self.surface)
        
        pygame.display.flip()

    def create_state(self):
        mouse_x , mouse_y = pygame.mouse.get_pos()
        can_create_circle = True
        for state in self.states:
            if state.is_too_close(StatesManager(mouse_x, mouse_y, self.index)):
                can_create_circle = False
                self.error_sound.play() 
                break
        if can_create_circle:
            self.states.append(StatesManager(mouse_x, mouse_y, self.index))
            self.index += 1

    def delete_state(self):
        mouse_x , mouse_y = pygame.mouse.get_pos()
        for state in self.states:
            if (mouse_x - state.x) ** 2 + (mouse_y - state.y) ** 2 <= state.radius ** 2:
                self.states.remove(state)

            for transition in state.transition_list:
                if ponto_proximo_linha(mouse_x, mouse_y, state.x, state.y, transition[0].x, transition[0].y):
                    state.transition_list.remove(transition)

    def select_state(self):
        if self.current_select_state == None:
            x, y = pygame.mouse.get_pos()
            for state in self.states:
                if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                        self.current_select_state = state
        else:
            print(self.current_select_state.transition_list)
            self.current_select_state = None

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
