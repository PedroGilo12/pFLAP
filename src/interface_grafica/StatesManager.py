import pygame

class StatesManager:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.radius = 50
        self.state_name = f"q{index + 1}"

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 153), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius, 2)

        font = pygame.font.Font(None, 20)
        text = font.render(self.state_name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def is_too_close(self, other_circle):
        distance_squared = (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        return distance_squared < (2 * self.radius) ** 2
