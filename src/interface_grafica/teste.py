import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Definição de algumas cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações da janela
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desenhar Linha com o Mouse")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill(BLACK)

    mouse_pos = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        pygame.draw.line(window, WHITE, (0,0), mouse_pos, 2)

    pygame.display.update()
