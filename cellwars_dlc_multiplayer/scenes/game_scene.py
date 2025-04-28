# game_scene.py
import pygame
import sys
from animated_connection import AnimatedConnection
from suggestion_handler import SuggestionHandler

import colors
from enemyAI import EnemyAI
from logger import setup_logger
from game_saver import GameSaver
from ui_renderer import UIRenderer
from input_handler import InputHandler




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


        self.pause_menu_buttons = [
            {"text": "SAVE", "rect": pygame.Rect(600, 20, 80, 30)},
            {"text": "MENU", "rect": pygame.Rect(500, 20, 80, 30)},
            {"text": "RESTART", "rect": pygame.Rect(400, 20, 80, 30)},
        ]

        self.main_button = {"text": "PAUSE", "rect": pygame.Rect(700, 20, 80, 30)}
        self.show_pause_menu = False


        self.font = pygame.font.SysFont(None, 20)
        self.context_font = pygame.font.SysFont("consolas", 10)
        self.logger, self.log_handler = setup_logger()
        self.font_log = pygame.font.SysFont("consolas", 10)

        self.ui_renderer = UIRenderer(
            font=self.font,
            load_font=self.font,       
            context_font=self.context_font,
            title_font=self.font,    
            logger=self.logger
        )

        self.input_handler = InputHandler(self)
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
        # zbierz unikalne kombinacje (owner, owner_id)
        owners = {
            (cell.owner, cell.owner_id)
            for cell in self.cells
            if cell.owner != "neutral" and cell.owner_id is not None
        }

        # najpierw gracze, posortowani po owner_id
        players = sorted(
            [o for o in owners if o[0] == "player"],
            key=lambda x: x[1]
        )
        # potem pozostali (np. enemy), posortowani po owner i owner_id
        others = sorted(
            [o for o in owners if o[0] != "player"],
            key=lambda x: (x[0], x[1])
        )

        return players + others

    def current_player(self):
        return self.turn_order[self.current_turn_index]

    def handle_events(self, events):
        return self.input_handler.handle(events)

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
            anim.update(self, shoot=shoot)


        self.animating_connections = [
            anim for anim in self.animating_connections if not anim.to_destroy
        ]

        # Warunki końca gry
        active_players = {(c.owner, c.owner_id) for c in self.cells if c.owner != "neutral"}

        if len(active_players) <= 1:
            self.game_over = True
            winner = next(iter(active_players)) if active_players else None

            winner = next(iter(active_players)) if active_players else None
            self.player_won = (winner and winner[0] == "player")

    def draw_button(self, screen, btn):
        mouse_over = btn["rect"].collidepoint(self.mouse_pos)
        base_color = (70, 70, 200)
        hover_color = (100, 100, 255)
        color = hover_color if mouse_over else base_color

        pygame.draw.rect(screen, color, btn["rect"], border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), btn["rect"], 2, border_radius=6)

        text = self.font.render(btn["text"], True, (255, 255, 255))
        text_rect = text.get_rect(center=btn["rect"].center)
        screen.blit(text, text_rect)

    def draw(self, screen: pygame.Surface):
        # 1) tło planszy
        screen.fill(colors.GRAY)

        # 2) animowane połączenia
        for anim in self.animating_connections:
            anim.draw(screen, offset=self.offset)

        # 3) linia przeciągania (jeśli trwa drag & connect)
        if self.dragging and self.selected:
            start = (self.selected.x + self.offset[0], self.selected.y + self.offset[1])
            end   = self.mouse_pos
            pygame.draw.line(screen, self.selected.color, start, end, 2)

        # 4) rysowanie wszystkich komórek
        for cell in self.cells:
            # przesuniecie + draw + przywrócenie oryginału
            ox, oy = cell.x, cell.y
            cell.x += self.offset[0]  
            cell.y += self.offset[1]
            cell.draw(screen)
            cell.x, cell.y = ox, oy

        # 5) UI
        self.ui_renderer.draw(self, screen)
