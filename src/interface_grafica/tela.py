import pygame
import sys
from ButtonBar import ButtonBar
from StatesManager import StatesManager

def main():
    pygame.init()
    pygame.mixer.init()

    screen_width, screen_height = 1350, 675 
    screen = pygame.display.set_mode((screen_width, screen_height)) 
    pygame.display.set_caption("pFlap")

    font = pygame.font.Font(None, 30)

    button_definitions = [
        {'position': (50, 10), 'size': (200, 50), 'color': (0, 0, 255), 'text': "Criar Estado"},
        {'position': (300, 10), 'size': (200, 50), 'color': (255, 0, 0), 'text': "Excluir Estado"}
    ]

    button_bar = ButtonBar(screen, font, button_definitions)

    running = True
    states = []
    error_sound = pygame.mixer.Sound("src/assets/snd_error.wav")
    index = 0
    action = "Criar Estado"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Botão direito do mouse
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botão esquerdo do mouse
                x, y = pygame.mouse.get_pos()
                if button_bar.button_area_rect.collidepoint(x, y):
                    for rect, _, _ in button_bar.buttons:
                        if rect.collidepoint(x, y):
                            # Altera o valor de action com base no texto do botão clicado
                            for button_definition in button_definitions:
                                if button_definition['position'] == rect.topleft:
                                    action = button_definition['text']
                                    break
                            break
                # cria novos estados
                elif action == "Criar Estado" and y - 50 > button_definitions[1]['position'][1] + 50:
                    can_create_circle = True
                    for state in states:
                        if state.is_too_close(StatesManager(x, y, index)):
                            can_create_circle = False
                            error_sound.play() 
                            break
                    if can_create_circle:
                        states.append(StatesManager(x, y, index))
                        index += 1
                # deleta estados já existentes
                elif action == "Excluir Estado":
                    x, y = pygame.mouse.get_pos()
                    for state in states:
                        if (x - state.x) ** 2 + (y - state.y) ** 2 <= state.radius ** 2:
                            states.remove(state)

        screen.fill((255, 255, 255))
        button_bar.draw()
        for state in states:
            state.draw(screen)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
