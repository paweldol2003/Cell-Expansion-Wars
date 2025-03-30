# game_scene.py
import pygame
import sys
from cell import Cell
from animated_connection import AnimatedConnection
import colors
from enemyAI import EnemyAI


def connect(a, b):
    if b not in a.connections:
        a.connections.append(b)

class GameScene:
    def __init__(self, cells, images):
        self.cells = cells
        self.images = images
        self.units = []
        self.selected = None
        self.dragging = False
        self.mouse_pos = (0, 0)
        self.timer = 0
        self.animating_connections = []
        self.enemy_ai = EnemyAI()


        self.buttons = [
            {"text": "MENU", "rect": pygame.Rect(700, 20, 80, 30)},
        ]
        self.font = pygame.font.SysFont(None, 30)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for cell in self.cells:
                    if cell.is_in_area(event.pos) and cell.owner == 'player':
                        self.selected = cell
                        self.dragging = True
                        break
                    elif self.selected and cell != self.selected and cell.is_in_area(event.pos):
                        connect(self.selected, cell)
                        self.animating_connections.append(AnimatedConnection(self.selected, cell))
                        self.selected = None

                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return 1

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging and self.selected:
                    for cell in self.cells:
                        if cell.is_in_area(event.pos):
                            if cell != self.selected:
                                connect(self.selected, cell)
                                self.animating_connections.append(AnimatedConnection(self.selected, cell))
                                self.selected = None
                            break
                    else:
                        self.selected = None
                self.dragging = False

    def update(self):
        self.timer += 1

        self.enemy_ai.update(self.cells, self.animating_connections)

        if self.timer >= 60:
            for cell in self.cells:
                if cell.owner != 'neutral':
                    cell.units += 1
            self.timer = 0

        for anim in self.animating_connections:
            anim.update(shoot=(self.timer == 50))

        self.animating_connections = [
            anim for anim in self.animating_connections if not getattr(anim, "to_destroy", False)
        ]


    def draw(self, screen: pygame.Surface):
        screen.fill(colors.GRAY)

        for anim in self.animating_connections:
            anim.draw(screen)

        if self.dragging and self.selected:
            pygame.draw.line(screen, colors.BLUE, (self.selected.x, self.selected.y), self.mouse_pos, 2)

        for cell in self.cells:
            cell.draw(screen)

        for btn in self.buttons:
            pygame.draw.rect(screen, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            screen.blit(text, (btn["rect"].x + 10, btn["rect"].y + 5))

        for unit in self.units:
            unit.draw(screen)
