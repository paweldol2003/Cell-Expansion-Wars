# cell.py
import pygame
import colors

class Cell:
    def __init__(self, x, y, radius, color, owner, type, image_map):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.owner = owner  # np. "player", "enemy", "neutral"
        self.units = 10
        self.type = type  # np. "normal", "fort", itd.
        self.connections = []
        self.image_map = image_map  # słownik z obrazkami

    @property
    def image(self):
        key = f"ID_UNIT_{self.owner.upper()}_{self.type.upper()}"
        raw_image = self.image_map.get(key)
        if raw_image:
            size = self.radius * 2
            return pygame.transform.smoothscale(raw_image, (size, size))
        else:
            print(f"Brak obrazka dla: {key}")
            return None

    def draw(self, WINDOW):
        img = self.image
        if img:
            img_rect = img.get_rect(center=(self.x, self.y))
            WINDOW.blit(img, img_rect)
        else:
            pygame.draw.circle(WINDOW, self.color, (self.x, self.y), self.radius)

        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.units), True, colors.WHITE)
        WINDOW.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def is_in_area(self, pos):
        dx = self.x - pos[0]
        dy = self.y - pos[1]
        return dx * dx + dy * dy <= self.radius * self.radius
