import pygame
import sys

class MenuScene:
    def __init__(self, images):
        self.images = images
        self.multi = False
        self.online = False  # nowa zmienna stanu
        self.font = pygame.font.SysFont(None, 36)

        self.buttons = [
            {"text": "Singleplayer", "multi": False, "rect": pygame.Rect(250, 100, 200, 50), "type": "mode"},
            {"text": "Multiplayer",  "multi": True,  "rect": pygame.Rect(470, 100, 200, 50), "type": "mode"},

            {"text": "Poziom 1", "stage": "stage_1",         "rect": pygame.Rect(300, 200, 200, 50), "type": "single"},
            {"text": "Poziom 2", "stage": "stage_2",         "rect": pygame.Rect(300, 270, 200, 50), "type": "single"},
            {"text": "Poziom 3", "stage": "stage_3",         "rect": pygame.Rect(300, 340, 200, 50), "type": "single"},

            {"text": "Poziom 1 (Multi)", "stage": "stage_1_multi", "rect": pygame.Rect(300, 200, 200, 50), "type": "multi"},

            # Nowe przyciski dla trybu multiplayer
            {"text": "Local",  "rect": pygame.Rect(250, 160, 200, 40), "type": "net_mode", "online": False},
            {"text": "Online", "rect": pygame.Rect(470, 160, 200, 40), "type": "net_mode", "online": True},
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["type"] == "mode":
                            self.multi = btn["multi"]
                        elif btn["type"] == "net_mode" and self.multi:
                            self.online = btn["online"]
                        elif (self.multi and btn["type"] == "multi") or (not self.multi and btn["type"] == "single"):
                            return btn["stage"]
        return None

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        for btn in self.buttons:
            show = False
            if btn["type"] == "mode":
                show = True
            elif btn["type"] == "single" and not self.multi:
                show = True
            elif btn["type"] == "multi" and self.multi:
                show = True
            elif btn["type"] == "net_mode" and self.multi:
                show = True

            if show:
                hovered = btn["rect"].collidepoint(mouse_pos)
                
                # Kolory
                if btn["type"] == "mode":
                    color = (100, 200, 100) if btn["multi"] == self.multi else (70, 70, 200)
                elif btn["type"] == "net_mode":
                    color = (100, 150, 250) if btn["online"] == self.online else (70, 70, 200)
                else:
                    color = (70, 70, 200)

                if hovered:
                    color = tuple(min(255, c + 40) for c in color)

                pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
                text = self.font.render(btn["text"], True, (255, 255, 255))
                text_rect = text.get_rect(center=btn["rect"].center)
                screen.blit(text, text_rect)
