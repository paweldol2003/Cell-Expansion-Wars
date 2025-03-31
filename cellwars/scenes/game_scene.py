# game_scene.py
import pygame
import sys
from cell import Cell
from animated_connection import AnimatedConnection
import colors
from enemyAI import EnemyAI

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
        self.animated_bullets = []

        self.enemy_ai = EnemyAI()

        self.buttons = [
            {"text": "MENU", "rect": pygame.Rect(700, 20, 80, 30)},
        ]
        self.font = pygame.font.SysFont(None, 30)

        # System rund
        self.round_timer = 0
        self.round_duration = 4 * 60  # 4 sekund w klatkach (zakładając 60 FPS)
        self.player_turn = True  # True = gracz, False = AI

        # Stan gry
        self.game_over = False
        self.player_won = False

    def connect(self, a, b):
        if b not in a.connections:
            a.connections.append(b)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return 1

                if not self.player_turn or self.game_over:
                    return

                for cell in self.cells:
                    if cell.is_in_area(event.pos) and cell.owner == 'player':
                        self.selected = cell
                        self.dragging = True
                        break
                    elif self.selected and cell != self.selected and cell.is_in_area(event.pos) and cell not in self.selected.connections:
                        
                        self.animating_connections.append(AnimatedConnection(self.selected, cell))
                        self.selected = None

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging and self.selected:
                    for cell in self.cells:
                        if cell.is_in_area(event.pos):
                            if cell != self.selected and cell not in self.selected.connections:
                                
                                self.animating_connections.append(AnimatedConnection(self.selected, cell))
                                self.selected = None
                            break
                    else:
                        self.selected = None
                self.dragging = False

    def update(self):
        if self.game_over:
            return

        self.timer += 1
        self.round_timer += 1

        # Sprawdź warunek zwycięstwa
        if not any(cell.owner == 'enemy' for cell in self.cells):
            self.game_over = True
            self.player_won = True
            return

        # Sprawdź warunek przegranej
        if not any(cell.owner == 'player' for cell in self.cells):
            self.game_over = True
            self.player_won = False
            return

        # Zmiana rundy co 4 sekundy
        if self.round_timer >= self.round_duration:
            self.player_turn = not self.player_turn
            self.round_timer = 0

        if not self.player_turn:
            self.enemy_ai.update(self.cells, self.animating_connections)

        if self.timer >= 60:
            for cell in self.cells:
                if cell.owner != 'neutral':
                    cell.units += 1
            self.timer = 0

        for anim in self.animating_connections:
            anim.update(shoot=(self.timer == 50))

        # self.animating_connections = [
        #     anim for anim in self.animating_connections if not getattr(anim, "to_destroy", False)
        # ]


    def draw(self, screen: pygame.Surface):
        screen.fill(colors.GRAY)

        for anim in self.animating_connections:
            anim.draw(screen)

        if self.dragging and self.selected:
            pygame.draw.line(screen, colors.GREEN, (self.selected.x, self.selected.y), self.mouse_pos, 2)

        for cell in self.cells:
            cell.draw(screen)

        for btn in self.buttons:
            pygame.draw.rect(screen, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            screen.blit(text, (btn["rect"].x + 10, btn["rect"].y + 5))

        for unit in self.units:
            unit.draw(screen)


        # Pasek czasu rundy
        pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)  # czarna ramka
        bar_width = int((self.round_timer / self.round_duration) * 200)
        pygame.draw.rect(screen, (200, 200, 200), (20, 60, 200, 10))  # tło
        if self.player_turn:
            pygame.draw.rect(screen, colors.GREEN, (20, 60, bar_width, 10))  # zielony pasek
        else:
            pygame.draw.rect(screen, colors.RED, (20, 60, bar_width, 10))  # czerwony pasek


        # Informacja o rundzie lub stanie gry
        if self.game_over:
            pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)  # ramka
            result_text = "YOU WON" if self.player_won else "YOU LOST"
            info = self.font.render(result_text, True, colors.WHITE)
            screen.blit(info, (400, 60))
        else:
            status_text = "Your turn" if self.player_turn else "AI turn"
            round_info = self.font.render(status_text, True, colors.WHITE)
            screen.blit(round_info, (20, 20))
