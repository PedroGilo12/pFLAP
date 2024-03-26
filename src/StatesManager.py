import pygame
import math
import time

class StatesManager:
    def __init__(self, x, y, index, initial=False, final=False):
        self.x = x
        self.y = y
        self.radius = 25
        self.initial = initial
        self.final = final
        self.state_name = f"q{index + 1}"
        self.transition_list = []
        
        self.scale = 1

    def draw(self, screen):
        list_of_transitions_marked = {}
        
        for transition in self.transition_list:
            initial_offset = 50
            if transition[0] in list_of_transitions_marked:
                list_of_transitions_marked[transition[0]] = list_of_transitions_marked[transition[0]] + 1
                initial_offset = 50 * list_of_transitions_marked[transition[0]]
            else:
                list_of_transitions_marked[transition[0]] = 1
                
            if self.x == transition[0].x and self.y == transition[0].y:
                self.draw_curve(screen, (self.x - (self.radius * 0.5), self.y), (transition[0].x + (self.radius * 0.5), transition[0].y), offset=100 + initial_offset,signal=-1, symbol= transition[1])
            else:
                if transition[0].x < self.x:
                    self.draw_curve(screen, (self.x, self.y), (transition[0].x, transition[0].y), offset=initial_offset, signal=-1,symbol= transition[1])
                else:
                    self.draw_curve(screen, (self.x, self.y), (transition[0].x, transition[0].y), offset=initial_offset, signal=1, symbol= transition[1])


        if self.final:
            line_width = 4
        else:
            line_width = 2
            
        if self.initial:
            self.draw_triangle(screen, self.x, self.y)
        
        scaled_x = int(self.x * self.scale)
        scaled_y = int(self.y * self.scale)
        scaled_radius = int(self.radius * self.scale)
        
        pygame.draw.circle(screen, (255, 255, 153), (scaled_x, scaled_y), scaled_radius)
        pygame.draw.circle(screen, (0, 0, 0), (scaled_x, scaled_y), scaled_radius, line_width)
        
        font = pygame.font.Font(None, 20)
        text = font.render(self.state_name, True, (0, 0, 0))
        text_rect = text.get_rect(center=(scaled_x, scaled_y))
        screen.blit(text, text_rect)

    def draw_arrow(self, screen, color, start_pos, end_pos, symbol ,width=6, offset_arrow=60):
        pygame.draw.line(screen, color, start_pos, end_pos, width)
        
        delta_x = start_pos[0] - end_pos[0]
        delta_y = start_pos[1] - end_pos[1]
        
        ponto_medio_x = (start_pos[0] + end_pos[0]) // 2
        ponto_medio_y = (start_pos[1] + end_pos[1]) // 2

        fonte = pygame.font.Font(None, 30)
        texto = fonte.render(symbol, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(ponto_medio_x, ponto_medio_y-15))
        screen.blit(texto, texto_rect)
        
        angle_rad = math.atan2(delta_x, delta_y)
        angle_degree = math.degrees(angle_rad)
        
        length = math.sqrt(delta_x**2 + delta_y**2)
        
        dx = delta_x / length
        dy = delta_y / length
        
        x3 = end_pos[0] + dx * offset_arrow
        y3 = end_pos[1] + dy * offset_arrow
        
        fonte = pygame.font.Font(None, 40)
        x = fonte.render("V", True, (0, 0, 0))
        rotated_x = pygame.transform.rotate(x, angle_degree + 180)
        
        text_rect = rotated_x.get_rect(center=(x3, y3))
        
        screen.blit(rotated_x, text_rect)

    def angle_degree(self, p1, p2):
        return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

    def draw_curve(self, window, p0, p2, offset, signal,symbol):
        if signal > 0:
            p1 = ((p0[0] + p2[0]) // 2, ((p0[1] + p2[1]) // 2) + offset)
        else:
            p1 = ((p0[0] + p2[0]) // 2, ((p0[1] + p2[1]) // 2) - offset)

        angle_deg = self.angle_degree(p1, p2)

        curve_points = []
        for t in range(0, 1000):
            t /= 1000.0
            x = int((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0])
            y = int((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])
            curve_points.append((x, y))
            pygame.draw.circle(window, (0,0,0), (x, y), 1)

        distance = math.sqrt((p2[0] - p0[0]) ** 2 + (p2[1] - p0[1]) ** 2)
        
        N = 900
        
        fonte = pygame.font.Font(None, 30)
        texto = fonte.render(symbol, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(curve_points[500][0], curve_points[500][1] + 12))
        window.blit(texto, texto_rect)
        
        #pygame.draw.circle(window, (255, 0, 0), (curve_points[500][0], curve_points[500][1] + 12), 5)

        n = min(len(curve_points) - 1, 1000 - (1000 - distance)*0.2)
        intermediate_point = curve_points[int(n)]

        arrow_length = 20
        arrow_end = (intermediate_point[0] + arrow_length * math.cos(math.radians(angle_deg)),
                    intermediate_point[1] + arrow_length * math.sin(math.radians(angle_deg)))
        pygame.draw.polygon(window, (0, 0, 0), (((arrow_end[0] + 10 * math.cos(math.radians(angle_deg + 135))),
                                            arrow_end[1] + 10 * math.sin(math.radians(angle_deg + 135))),
                                            (arrow_end[0] + 10 * math.cos(math.radians(angle_deg - 135)),
                                            arrow_end[1] + 10 * math.sin(math.radians(angle_deg - 135))),
                                            arrow_end))
        
    def remove_transition(self, pos_mouse):
        list_of_transitions_marked = {}
        
        for transition in self.transition_list:
            initial_offset = 50
            if transition[0] in list_of_transitions_marked:
                list_of_transitions_marked[transition[0]] = list_of_transitions_marked[transition[0]] + 1
                initial_offset = 50 * list_of_transitions_marked[transition[0]]
            else:
                list_of_transitions_marked[transition[0]] = 1
                
            if self.x == transition[0].x and self.y == transition[0].y:
                if self.is_clicked(5,(self.x - (self.radius * 0.5), self.y), (transition[0].x + (self.radius * 0.5), transition[0].y), (pos_mouse[0], pos_mouse[1]), 100 + initial_offset, -1):
                    self.transition_list.remove(transition)
            else:
                if transition[0].x < self.x:
                    if self.is_clicked(5, (self.x, self.y), (transition[0].x, transition[0].y), (pos_mouse[0], pos_mouse[1]), initial_offset, -1):
                        self.transition_list.remove(transition)
                else:
                    if self.is_clicked(5, (self.x, self.y), (transition[0].x, transition[0].y), (pos_mouse[0], pos_mouse[1]), initial_offset, 1):
                        self.transition_list.remove(transition)

    def is_clicked(self, limit, p0, p2, p, offset, signal):
        if signal > 0:
            p1 = ((p0[0] + p2[0]) // 2, ((p0[1] + p2[1]) // 2) + offset)
        else:
            p1 = ((p0[0] + p2[0]) // 2, ((p0[1] + p2[1]) // 2) - offset)


        curve_points = []
        for t in range(0, 1000):
            t /= 1000.0
            x = int((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0])
            y = int((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])
            curve_points.append((x, y))

        distance = math.sqrt((curve_points[500][0] - p[0]) ** 2 + ((curve_points[500][1] + 12) - p[1]) ** 2)
        
        return distance <= limit
            
    def draw_triangle(self, screen, x, y):
        x3 = x + 50 * math.cos(math.pi +  math.pi / 6)
        y3 = y + 50 * math.sin(math.pi + math.pi / 6)
        x4 = x + 50 * math.cos(math.pi - math.pi / 6)
        y4 = y + 50 * math.sin(math.pi - math.pi / 6)

        pygame.draw.polygon(screen, (0,0,0), [(x, y), (x3, y3), (x4, y4)])

    def draw_return_arrow(self, screen,x, y, color, R, C, symbol):
        
        delta_x = (x - (R*0.3)) - (x - (R))
        delta_y = y - (y - C)
        
        length = math.sqrt(delta_x**2 + delta_y**2)
        
        dx = delta_x / length
        dy = delta_y / length
        
        x3 = (x - (R)) + dx * 25
        y3 = (y - C) + dy * 25
        
        angle_rad = math.atan2(delta_x, delta_y)
        angle_degree = math.degrees(angle_rad)

        fonte = pygame.font.Font(None, 30)
        texto = fonte.render(symbol, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(x, y-(R + C)))
        screen.blit(texto, texto_rect)
        
        pygame.draw.line(screen, color, (x - (R*0.7), y - (R*0.7)), (x - (R), y - C), 5)
        
        pygame.draw.line(screen, color, (x + (R*0.7), y - (R*0.7)), (x + (R), y - C), 5)
        
        pygame.draw.line(screen, color, (x + R, y - C), (x - R, y - C), 5)
        
        fonte = pygame.font.Font(None, 50)
        text = fonte.render("V", True, (0, 0, 0))
        rotated_x = pygame.transform.rotate(text, angle=angle_degree)
        text_rect = rotated_x.get_rect(center= (x3, y3))
        screen.blit(rotated_x, text_rect)


    def add_transition(self, state, symbol):
        print("Adicionando transição para ", self.state_name)
        self.transition_list.append([state, symbol])

    def is_too_close(self, other_circle):
        distance_squared = (self.x - other_circle.x) ** 2 + (self.y - other_circle.y) ** 2
        return distance_squared < (2 * self.radius) ** 2
