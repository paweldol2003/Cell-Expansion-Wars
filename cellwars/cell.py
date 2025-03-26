# cell.py
import pygame


WHITE = (255, 255, 255)

class Cell:
    def __init__(self, x, y, radius, color, owner, type):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.owner = owner
        self.units = 10
        self.type = type
        self.connections = []


    def draw(self, WINDOW):
        pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.radius)
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.units), True, WHITE)
        WINDOW.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def is_clicked(self, pos):
        dx = self.x - pos[0]
        dy = self.y - pos[1]
        return dx * dx + dy * dy <= self.radius * self.radius
