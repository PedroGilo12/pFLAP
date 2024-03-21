import pygame

class ButtonBar:
    def __init__(self, screen, font, button_definitions):
        self.screen = screen
        self.font = font
        self.buttons = []
        self.button_area_rect = pygame.Rect(0, 0, screen.get_width(), 70)
        self.button_area_color = (200, 200, 200)
        self.add_buttons_from_definitions(button_definitions)

    def add_button(self, rect, color, text):
        self.buttons.append((rect, color, text))

    def add_buttons_from_definitions(self, button_definitions):
        for definition in button_definitions:
            rect = pygame.Rect(definition['position'], definition['size'])
            color = definition['color']
            text = definition['text']
            self.add_button(rect, color, text)

    def draw(self):
        pygame.draw.rect(self.screen, self.button_area_color, self.button_area_rect)
        for rect, color, text in self.buttons:
            pygame.draw.rect(self.screen, color, rect)
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
