import pygame
import sys
from ButtonBar import ButtonBar
from StatesManager import StatesManager

class Screen():
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        pygame.display.set_caption("pFlap")

        font = pygame.font.Font(None, 30)

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
                        
                # deleta estados já existentes
                elif self.action == "Excluir Estado":
                    x, y = pygame.mouse.get_pos()
                    for state in self.states:
                        if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                            self.states.remove(state)

        self.screen.fill((255, 255, 255))
        self.button_bar.draw()
        for state in self.states:
            state.draw(self.screen)
        
        pygame.display.flip()