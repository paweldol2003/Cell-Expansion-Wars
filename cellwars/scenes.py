import pygame
from cell import Cell
import stages
import sys


# Kolory
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
RED = (220, 20, 60)

def connect(a, b):
    if b not in a.connections:
        a.connections.append(b)
    if a not in b.connections:
        b.connections.append(a)



class GameScene:


    def __init__(self, cells):
        self.cells = cells
        self.units = []
        self.selected = None
        self.timer = 0
        self.buttons = [
            {"text": "MENU", "rect": pygame.Rect(700, 20, 80, 30)},
        ]
        self.font = pygame.font.SysFont(None, 30)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for cell in self.cells: #do wyrzucenia pózniej
                    if cell.is_clicked(event.pos):
                        if self.selected is None and cell.owner == 'player':
                            self.selected = cell
                        elif self.selected and cell != self.selected:
                            print(f"Wysyłanie jednostek z {self.selected} do {cell}")
                            self.selected.units -= 1
                            cell.units -= 1
                            connect(self.selected, cell)
                            self.selected.connections.append(cell)
                            self.selected = None

                            


                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return 1


    def update(self):
        self.timer += 1
        if self.timer >= 60:  # co 60 klatek = 1 sekunda
            for cell in self.cells:
                cell.units += 1

            

            self.timer = 0

    def draw(self, WINDOW):
        WINDOW.fill(GRAY)
        for cell in self.cells:
            for connected in cell.connections:
                pygame.draw.line(WINDOW, (100, 100, 100), (cell.x, cell.y), (connected.x, connected.y), 3)

        for cell in self.cells:
            cell.draw(WINDOW)
        for btn in self.buttons:
            pygame.draw.rect(WINDOW, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            WINDOW.blit(text, (btn["rect"].x+10, btn["rect"].y+5))
        for unit in self.units:
            unit.draw(WINDOW)

class MenuScene:
    def __init__(self):
        self.buttons = [
            {"text": "Poziom 1", "stage": stages.get_stage_1, "rect": pygame.Rect(300, 200, 200, 50)},
            {"text": "Poziom 2", "stage": stages.get_stage_2, "rect": pygame.Rect(300, 300, 200, 50)},
        ]
        self.font = pygame.font.SysFont(None, 36)

    def handle_events(self, events):
        for event in events:
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

    def draw(self, WINDOW):
        WINDOW.fill((30, 30, 30))
        for btn in self.buttons:
            pygame.draw.rect(WINDOW, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            WINDOW.blit(text, (btn["rect"].x + 50, btn["rect"].y + 10))
  