# game_scene.py
import pygame
import sys
from ui import UI
from game_logic import GameLogic
from connections_handler import ConnectionHandler
from AI_suggestions import AI
from event_handler import EventHandler
from logger import setup_logger
import colors


class GameScene:
    def __init__(self, cells, images):
        self.cells = cells
        self.images = images
        self.offset = [0, 0]
        self.mouse_pos = (0, 0)

        # Fonty
        self.font = pygame.font.SysFont(None, 30)
        self.context_font = pygame.font.SysFont("consolas", 10)

        # Logger
        self.logger, self.log_handler = setup_logger()

        # UI
        self.ui = UI(self.font, self.log_handler)
        self.buttons = [{"text": "MENU", "rect": pygame.Rect(700, 20, 80, 30)}]

        # Logika i AI
        self.game_logic = GameLogic()
        self.connection_handler = ConnectionHandler()
        self.ai = AI()
        self.event_handler = EventHandler(self.cells, self.logger, self.connection_handler)

        # Interakcja
        self.context_cell = None
        self.context_menu_pos = None
        self.context_menu_visible = False
        self.selection_timer = 0
        self.suggestion = None

    def handle_event(self, event):
        return self.event_handler.handle_event(event, self)


    def update(self):
        if self.game_logic.game_over:
            return

        self.selection_timer += 1
        self.game_logic.update(self.cells)

        if self.game_logic.round_timer == 1 and self.game_logic.player_turn:
            self.suggestion = self.ai.generate_suggestion(self.cells)

        if not self.game_logic.player_turn:
            self.ai.enemy_turn(self.cells, self.connection_handler.animating_connections)

        if self.game_logic.timer >= 60:
            for cell in self.cells:
                if cell.owner != 'neutral':
                    cell.units += 1
            self.game_logic.timer = 0

        self.connection_handler.update_connections(self.game_logic.timer)

    def draw(self, screen: pygame.Surface):
        screen.fill(colors.GRAY)

        # Rysowanie animowanych połączeń
        for anim in self.connection_handler.animating_connections:
            anim.draw(screen, offset=self.offset)

        # Rysowanie linii przeciągania
        if self.event_handler.dragging and self.event_handler.selected:
            pygame.draw.line(
                screen, colors.GREEN,
                (self.event_handler.selected.x + self.offset[0], self.event_handler.selected.y + self.offset[1]),
                self.mouse_pos, 2
            )

        # Rysowanie komórek
        for cell in self.cells:
            original_x, original_y = cell.x, cell.y
            cell.x += self.offset[0]
            cell.y += self.offset[1]
            cell.draw(screen)
            cell.x, cell.y = original_x, original_y

        # UI
        self.ui.draw_buttons(screen, self.buttons)
        self.ui.draw_status(screen, self.game_logic.game_over, self.game_logic.player_won, self.game_logic.player_turn)

        # Pasek tury
        self.ui.draw_turn_bar(
            screen,
            self.game_logic.round_timer,
            self.game_logic.round_duration,
            self.game_logic.player_turn
        )


        # Podświetlenia
        self.draw_selection_highlight(screen)

        # Menu kontekstowe
        self.draw_context_menu(screen)

        # Sugerowany ruch
        self.draw_suggestion(screen)

        # Logi
        self.ui.draw_logs(screen)


    def draw_selection_highlight(self, screen):
        if self.event_handler.selected:
            ox, oy = self.offset
            for cell in self.cells:
                if cell != self.event_handler.selected and cell not in self.event_handler.selected.connections:
                    cx = cell.x + ox
                    cy = cell.y + oy
                    pulse_radius = cell.radius + 4 + (self.selection_timer % 100) // 3
                    alpha = max(0, 255 - (self.selection_timer % 100) * 4)
                    ring_surface = pygame.Surface((pulse_radius * 2 + 4, pulse_radius * 2 + 4), pygame.SRCALPHA)
                    pygame.draw.circle(
                        ring_surface,
                        (0, 255, 0, alpha),
                        (pulse_radius + 2, pulse_radius + 2),
                        pulse_radius,
                        3
                    )
                    screen.blit(ring_surface, (cx - pulse_radius - 2, cy - pulse_radius - 2))

            # Obramowanie komórki
            sel_x = self.event_handler.selected.x + ox
            sel_y = self.event_handler.selected.y + oy
            pygame.draw.circle(screen, (255, 255, 0), (sel_x, sel_y), self.event_handler.selected.radius + 6, 4)

    def draw_context_menu(self, screen):
        if self.context_menu_visible and self.context_cell:
            x, y = self.context_menu_pos
            menu_width = 220
            item_height = 36
            padding = 8
            border_radius = 8

            for idx, target in enumerate(self.context_cell.connections):
                rect = pygame.Rect(x, y + idx * (item_height + padding), menu_width, item_height)
                shadow_rect = rect.copy().move(2, 2)
                pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=border_radius)
                pygame.draw.rect(screen, (40, 40, 40), rect, border_radius=border_radius)
                pygame.draw.rect(screen, (120, 120, 120), rect, width=1, border_radius=border_radius)

                text_label = f"{idx+1}. Usuń połączenie z ({target.x}, {target.y})"
                text_surface = self.context_font.render(text_label, True, (240, 240, 240))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    def draw_suggestion(self, screen):
        if self.suggestion:
            src, tgt = self.suggestion
            src_pos = (src.x + self.offset[0], src.y + self.offset[1])
            tgt_pos = (tgt.x + self.offset[0], tgt.y + self.offset[1])
            pygame.draw.line(screen, (0, 255, 255), src_pos, tgt_pos, 3)
            tip_text = self.font.render("Sugerowany ruch", True, (0, 255, 255))
            screen.blit(tip_text, (20, 90))
