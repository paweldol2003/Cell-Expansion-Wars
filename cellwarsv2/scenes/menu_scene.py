# menu_scene.py
import pygame
import sys

class MenuScene:
    def __init__(self, images):
        self.images = images
        self.buttons = [
            {"text": "Poziom 1", "stage": "stage_1", "rect": pygame.Rect(300, 200, 200, 50)},
            {"text": "Poziom 2", "stage": "stage_2", "rect": pygame.Rect(300, 300, 200, 50)},
            {"text": "Poziom 3", "stage": "stage_3", "rect": pygame.Rect(300, 400, 200, 50)},
        ]
        self.font = pygame.font.SysFont(None, 36)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    return btn["stage"]
        return None

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill((30, 30, 30))
        for btn in self.buttons:
            pygame.draw.rect(screen, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            screen.blit(text, (btn["rect"].x + 50, btn["rect"].y + 10))
