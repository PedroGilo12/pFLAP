import pygame
import math

class StatesManager:
    def __init__(self, x, y, index, initial=False, final=False):
        self.x = x
        self.y = y
        self.radius = 25
        self.initial = initial
        self.final = final
        self.state_name = f"q{index + 1}"
        self.transition_list = []

    def draw(self, screen):
        for transition in self.transition_list:
            if self.x == transition[0].x and self.y == transition[0].y:
                self.draw_arrow_return(screen, self.x, self.y, transition[0].x, transition[0].y,  transition[1])
            else:
                self.draw_arrows(screen, self.x, self.y, transition[0].x, transition[0].y, transition[1])

        if self.final:
            line_width = 4
        else:
            line_width = 2
        
        pygame.draw.circle(screen, (255, 255, 153), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius, line_width)
        
        font = pygame.font.Font(None, 20)
        text = font.render(self.state_name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)
        
    def draw_arrows(self, screen, x1, y1, x2, y2, symbol, cor_linha=(0, 0, 0), comprimento_ponta=50, largura_ponta=8):
        # Calcule o ângulo da linha
        angulo = math.atan2(y2 - y1, x2 - x1)

        # Calcule o ponto médio da linha
        ponto_medio_x = (x1 + x2) // 2
        ponto_medio_y = (y1 + y2) // 2

        # Desenhe o texto no ponto médio da linha
        fonte = pygame.font.Font(None, 30)
        texto = fonte.render(symbol, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(ponto_medio_x, ponto_medio_y-7))
        screen.blit(texto, texto_rect)

        # Desenhe a linha na tela
        pygame.draw.line(screen, cor_linha, (x1, y1), (x2, y2), 5)

        # Calcule as coordenadas da ponta da seta
        x3 = x2 - comprimento_ponta * math.cos(angulo + math.pi / 6)
        y3 = y2 - comprimento_ponta * math.sin(angulo + math.pi / 6)
        x4 = x2 - comprimento_ponta * math.cos(angulo - math.pi / 6)
        y4 = y2 - comprimento_ponta * math.sin(angulo - math.pi / 6)

        # Desenhe a ponta da seta
        pygame.draw.polygon(screen, cor_linha, [(x2, y2), (x3, y3), (x4, y4)])

    def draw_arrow_return(self, screen, x1, y1, x2, y2, symbol,cor_linha=(0, 0, 0), comprimento_ponta=50, largura_ponta=8):
        pygame.draw.line(screen, cor_linha, (x1-(self.radius/2), y1+(self.radius/2)), (x1, y1-(self.radius*2)), 5)
        pygame.draw.line(screen, cor_linha, (x1, y1-(self.radius*2)), (x1+(self.radius/2), y1), 5)
        
        # Desenhe o texto no ponto médio da linha
        fonte = pygame.font.Font(None, 30)
        texto = fonte.render(symbol, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(x1 + 10, y1 + 10))
        screen.blit(texto, texto_rect)


    def add_transition(self, state, symbol):
        print("Adicionando transição para ", self.state_name)
        self.transition_list.append([state, symbol])

    def is_too_close(self, other_circle):
        distance_squared = (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        return distance_squared < (2 * self.radius) ** 2
