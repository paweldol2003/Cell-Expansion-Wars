# game_scene.py
import pygame
import sys
from animated_connection import AnimatedConnection
from suggestion_handler import SuggestionHandler

import colors
from enemyAI import EnemyAI
from logger import setup_logger
from game_saver import GameSaver


class GameScene:
    def __init__(self, cells, images):
        self.cells = cells
        self.images = images
        self.selected = None
        self.dragging = False
        self.mouse_pos = (0, 0)
        self.timer = 0
        self.round_duration = 4 * 60  # 4 sekund w klatkach (zakładając 60 FPS)
        self.player_turn = True  # True = gracz, False = AI
        self.turn_order = self.compute_turn_order()
        self.current_turn_index = 0

        self.animating_connections = []
        self.animated_bullets = []
        self.context_cell = None  # komórka, na której otwarto menu
        self.context_menu_pos = None  # gdzie wyświetlić menu
        self.context_menu_visible = False

        self.enemy_ai = EnemyAI()
        self.suggestion_handler = SuggestionHandler()


        self.buttons = [
            {"text": "PAUSE", "rect": pygame.Rect(700, 20, 80, 30)},
            {"text": "SAVE", "rect": pygame.Rect(600, 20, 80, 30)},
            {"text": "MENU", "rect": pygame.Rect(500, 20, 80, 30)},
            {"text": "RESTART", "rect": pygame.Rect(400, 20, 80, 30)},
        ]

        self.font = pygame.font.SysFont(None, 30)
        self.context_font = pygame.font.SysFont("consolas", 10)
        self.logger, self.log_handler = setup_logger()
        self.font_log = pygame.font.SysFont("consolas", 10)

        # Przesuwanie
        self.offset = [0, 0]         # globalne przesunięcie planszy
        self.is_panning = False      # flaga aktywnego przesuwania
        self.pan_start = (0, 0)

        # Stan gry
        self.game_over = False
        self.pause = False
        self.player_won = False #do zmiany
        self.winner = None

        self.history = [] 

    def compute_turn_order(self):
        return sorted(set(
            (cell.owner, cell.owner_id)
            for cell in self.cells
            if cell.owner != "neutral" and cell.owner_id is not None
        ), key=lambda x: (x[0], x[1]))

    def current_player(self):
        return self.turn_order[self.current_turn_index]

    def handle_events(self, events):
        for event in events:
            current_owner, current_owner_id = self.current_player()
            if current_owner != "player":
                return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # PPM
                    for cell in self.cells:
                        if cell.is_in_area(event.pos, self.offset) and cell.owner == "player" and cell.owner_id == current_owner_id:

                            self.context_cell = cell
                            self.context_menu_pos = event.pos
                            self.context_menu_visible = True
                            break
                    else:
                        self.context_menu_visible = False  # kliknięto poza komórką
                        self.is_panning = True
                        self.logger.info("Przesuwanie planszy")

                        self.pan_start = event.pos
                    return
                if event.button == 1 and self.context_menu_visible and self.context_cell:
                    x, y = self.context_menu_pos
                    for idx, target in enumerate(self.context_cell.connections):
                        rect = pygame.Rect(x, y + idx * 30, 200, 30)
                        if rect.collidepoint(event.pos):
                            self.logger.info(f"Usunięto połączenie z ({target.x}, {target.y})")

                            self.context_cell.connections.remove(target)

                            # Znajdź i zaznacz połączenie do usunięcia
                            for anim in self.animating_connections:
                                if anim.start_cell == self.context_cell and anim.end_cell == target:
                                    anim.mark_for_removal = True

                            self.context_menu_visible = False
                            return
                        
                for btn in self.buttons:
                    if btn["rect"].collidepoint(event.pos) and btn["text"] == "MENU":
                        return "menu"
                    elif btn["rect"].collidepoint(event.pos) and btn["text"] == "RESTART":
                        self.logger.info("Restart gry")
                        return "restart"
                    elif btn["rect"].collidepoint(event.pos) and btn["text"] == "PAUSE":
                        #tutaj będzie pauza
                        self.pause = not self.pause
                        if self.pause:
                            self.logger.info("Gra wznowiona")
                        else:
                            self.logger.info("Gra wstrzymana") 
                    elif btn["rect"].collidepoint(event.pos) and btn["text"] == "SAVE":
                        #cos jeszcze???
                        snapshot = {
                            "tick": self.timer,
                            "save_decision": "player",
                            "turn": self.current_player(),
                            "cells": self.cells,
                        }
                        self.history.append(snapshot)
                        GameSaver(self.history)
                        self.logger.info("Zapisano grę")

                if not self.player_turn or self.game_over:
                    return

                for cell in self.cells:
                    if cell.is_in_area(event.pos, self.offset) and cell.owner == 'player'and cell.owner_id == current_owner_id:
                        self.selected = cell
                        self.dragging = True
                        self.logger.info("Zaznaczono komorke")

                        break
                    if (
                        self.selected
                        and cell != self.selected
                        and cell.is_in_area(event.pos, self.offset)
                        and cell not in self.selected.connections
                    ):
                        # LIMIT: max 2 połączenia, HEX = 3
                        max_conns = 3 if self.selected.type == "hex" else 2
                        if len(self.selected.connections) >= max_conns:
                            self.logger.info("Osiągnięto limit połączeń dla tej komórki.")
                            self.selected = None
                            return

                        self.animating_connections.append(AnimatedConnection(self.selected, cell))
                        self.selected = None


            elif event.type == pygame.MOUSEMOTION:
                if self.is_panning:
                    dx = event.pos[0] - self.pan_start[0]
                    dy = event.pos[1] - self.pan_start[1]
                    self.offset[0] += dx
                    self.offset[1] += dy
                    self.pan_start = event.pos
                else:
                    self.mouse_pos = event.pos


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.is_panning = False
                if self.dragging and self.selected:
                    for cell in self.cells:
                        if cell.is_in_area(event.pos, self.offset):
                            if cell != self.selected and cell not in self.selected.connections:
                                max_conns = 3 if self.selected.type == "hex" else 2
                                if len(self.selected.connections) >= max_conns:
                                    self.logger.info("Osiągnięto limit połączeń dla tej komórki.")
                                    self.selected = None
                                    return
                                self.animating_connections.append(AnimatedConnection(self.selected, cell))
                                self.selected = None
                            break
                    else:
                        self.selected = None
                self.dragging = False

            elif event.type == pygame.KEYDOWN: # włącz/wyłącz sugestie
                if event.key == pygame.K_SPACE:
                    self.suggestion_handler.toggle()


    def update(self):
        if self.game_over:
            return

        self.timer += 1

        # Zmiana tury co round_duration
        if self.timer % self.round_duration == 0:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)

        current_owner, current_owner_id = self.current_player()

        # Generowanie sugestii dla gracza
        if current_owner == "player" and self.timer % self.round_duration == 1:
            self.suggestion_handler.generate([
                c for c in self.cells if c.owner == "player" and c.owner_id == current_owner_id
            ])

        # AI ruch
        if current_owner == "enemy":
            self.enemy_ai.update(
                owner_id=current_owner_id,
                cells=self.cells,
                animating_connections=self.animating_connections
            )


        # Przyrost jednostek co sekundę
        if self.timer % 60 == 0:
            for cell in self.cells:
                if cell.owner != "neutral":
                    cell.units += 1

        # Historia gry
        snapshot = {
            "tick": self.timer,
            "save_decision": "system",
            "turn": self.current_player(),
            "cells": self.cells,
        }
        self.history.append(snapshot)

        # Strzelanie co 50 klatek
        shoot = (self.timer % 50 == 0)
        for anim in self.animating_connections:
            anim.update(shoot=shoot)

        self.animating_connections = [
            anim for anim in self.animating_connections if not getattr(anim, "to_destroy", False)
        ]

        # Warunki końca gry
        active_players = {(c.owner, c.owner_id) for c in self.cells if c.owner != "neutral"}

        if len(active_players) <= 1:
            self.game_over = True
            winner = next(iter(active_players)) if active_players else None

            winner = next(iter(active_players)) if active_players else None
            self.player_won = (winner and winner[0] == "player")





    def draw(self, screen: pygame.Surface):
        screen.fill(colors.GRAY)

        # Rysowanie animowanych połączeń
        for anim in self.animating_connections:
            anim.draw(screen, offset=self.offset)

        # Rysowanie linii przeciągania (jeśli zaznaczono komórkę)
        if self.dragging and self.selected:
            pygame.draw.line(screen, self.selected.color,
                            (self.selected.x + self.offset[0], self.selected.y + self.offset[1]),
                            (self.mouse_pos[0], self.mouse_pos[1]), 2)

        # Rysowanie komórek z uwzględnieniem offsetu
        for cell in self.cells:
            # Zachowujemy oryginalne pozycje
            original_x, original_y = cell.x, cell.y
            cell.x += self.offset[0]
            cell.y += self.offset[1]
            cell.draw(screen)
            # Przywracamy pierwotne współrzędne
            cell.x, cell.y = original_x, original_y

        # Rysowanie przycisków
        for btn in self.buttons:
            pygame.draw.rect(screen, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            screen.blit(text, (btn["rect"].x + 10, btn["rect"].y + 5))


        # Pasek czasu rundy
        pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)  # ramka
        bar_width = int((self.timer % self.round_duration) / self.round_duration * 200)
        pygame.draw.rect(screen, (200, 200, 200), (20, 60, 200, 10))  # tło paska
        if self.player_turn:
            pygame.draw.rect(screen, colors.GREEN, (20, 60, bar_width, 10))
        else:
            pygame.draw.rect(screen, colors.RED, (20, 60, bar_width, 10))

        # Informacja o stanie gry
        if self.game_over:
            pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)
            if self.winner:
                who, idx = self.winner
                result_text = f"{who.capitalize()} {idx} wins!"
            else:
                result_text = "DRAW"

            info = self.font.render(result_text, True, colors.WHITE)
            screen.blit(info, (400, 60))
        else:
            owner, owner_id = self.current_player()
            status_text = f"{owner.capitalize()} {owner_id}'s turn"
            round_info = self.font.render(status_text, True, colors.WHITE)
            screen.blit(round_info, (20, 20))
        # Wyświetlanie logów w rogu ekranu
        log_lines = self.log_handler.get_logs()
        log_x, log_y = 10, screen.get_height() - 20 * len(log_lines) - 10

        # Animowane podświetlenie zaznaczonej komórki
        if self.selected:
            ox, oy = self.offset

            for cell in self.cells:
                if cell != self.selected and cell not in self.selected.connections:
                    cx = cell.x + ox
                    cy = cell.y + oy

                    # Animacja pulsującego pierścienia
                    if self.selected.owner == cell.owner and self.selected.type == "defence" or self.selected.owner != cell.owner and self.selected.type == "attack":
                        pulse_radius = cell.radius + 4 + (self.timer % 50) // 3
                        alpha = max(0, 255 - (self.timer % 50) * 4)
                    else:
                        pulse_radius = cell.radius + 4 + (self.timer % 100) // 3
                        alpha = max(0, 255 - (self.timer % 100) * 4)
                    ring_surface = pygame.Surface((pulse_radius * 2 + 4, pulse_radius * 2 + 4), pygame.SRCALPHA)
                    pygame.draw.circle(
                        ring_surface,
                        (0, 255, 0, alpha),
                        (pulse_radius + 2, pulse_radius + 2),
                        pulse_radius,
                        3
                    )

                    screen.blit(ring_surface, (cx - pulse_radius - 2, cy - pulse_radius - 2))
                    pulse_radius = cell.radius + 4 + (self.timer % 100) // 3
                    alpha = max(0, 255 - (self.timer % 100) * 4)

                    ring_surface = pygame.Surface((pulse_radius * 2 + 4, pulse_radius * 2 + 4), pygame.SRCALPHA)
                    pygame.draw.circle(ring_surface,(255, 255, 0, alpha),(pulse_radius + 2, pulse_radius + 2),pulse_radius,3)

                    screen.blit(ring_surface, (cx - pulse_radius - 2, cy - pulse_radius - 2))

            # Dodatkowe obramowanie na samej zaznaczonej komórce
            sel_x = self.selected.x + ox
            sel_y = self.selected.y + oy
            pygame.draw.circle(screen, (255, 255, 0), (sel_x, sel_y), self.selected.radius + 6, 4)

        if self.context_menu_visible and self.context_cell:
            x, y = self.context_menu_pos
            menu_width = 220
            item_height = 36
            padding = 8
            border_radius = 8

            for idx, target in enumerate(self.context_cell.connections):
                rect = pygame.Rect(x, y + idx * (item_height + padding), menu_width, item_height)

                # Tło z lekkim cieniem
                shadow_rect = rect.copy()
                shadow_rect.move_ip(2, 2)
                pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=border_radius)

                # Główne tło
                pygame.draw.rect(screen, (40, 40, 40), rect, border_radius=border_radius)

                # Obrys
                pygame.draw.rect(screen, (120, 120, 120), rect, width=1, border_radius=border_radius)

                # Numerowana etykieta
                text_label = f"{idx+1}. Usuń połączenie z ({target.x}, {target.y})"
                text_surface = self.context_font.render(text_label, True, (240, 240, 240))

                # Wyśrodkowanie w pionie
                text_rect = text_surface.get_rect()
                text_rect.center = rect.center

                screen.blit(text_surface, text_rect)

        if self.suggestion_handler.show and self.suggestion_handler.suggestion:
            src, tgt = self.suggestion_handler.suggestion
            src_pos = (src.x + self.offset[0], src.y + self.offset[1])
            tgt_pos = (tgt.x + self.offset[0], tgt.y + self.offset[1])
            pygame.draw.line(screen, (0, 255, 255), src_pos, tgt_pos, 3)

            tip_text = self.font.render("Sugerowany ruch", True, (0, 255, 255))
            screen.blit(tip_text, (20, 90))

        for line in log_lines:
            rendered = self.font_log.render(line, True, (255, 255, 0))
            screen.blit(rendered, (log_x, log_y))
            log_y += 20


