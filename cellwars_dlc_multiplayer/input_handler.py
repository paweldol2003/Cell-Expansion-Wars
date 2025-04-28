# input_handler.py
import pygame
import sys
from animated_connection import AnimatedConnection
from game_saver import GameSaver

class InputHandler:
    def __init__(self, scene):
        self.scene = scene

    def handle(self, events):
        """
        Procesuje eventy Pygame, modyfikuje stan sceny lub zwraca 'menu'/'restart'.
        """
        s = self.scene
        # pobierz raz, czyja jest tura
        current_owner, current_owner_id = s.current_player()

        for event in events:
            # ─── EXIT ALWAYS ────────────────────────────────────────
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ─── PAN (PPM down) ─────────────────────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                s.context_menu_visible = False
                s.is_panning = True
                s.pan_start = event.pos
                s.logger.info("Przesuwanie planszy")
                continue

            # ─── PAN END & CONTEXT-MENU (PPM up) ────────────────────
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                s.is_panning = False
                # tylko na Twojej turze pozwól otworzyć menu
                if current_owner == "player" and not s.game_over and s.player_turn:
                    for cell in s.cells:
                        if (cell.is_in_area(event.pos, s.offset)
                            and cell.owner == "player"
                            and cell.owner_id == current_owner_id):
                            s.context_cell = cell
                            s.context_menu_pos = event.pos
                            s.context_menu_visible = True
                            break
                    else:
                        s.context_menu_visible = False
                else:
                    s.context_menu_visible = False
                continue

            # ─── MOUSE MOTION (pan lub tracking) ────────────────────
            if event.type == pygame.MOUSEMOTION:
                if s.is_panning:
                    dx = event.pos[0] - s.pan_start[0]
                    dy = event.pos[1] - s.pan_start[1]
                    s.offset[0] += dx
                    s.offset[1] += dy
                    s.pan_start = event.pos
                else:
                    s.mouse_pos = event.pos
                continue

            # ─── PAUSE BUTTON (LPM) ──────────────────────────────────
            if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and s.main_button["rect"].collidepoint(event.pos)):
                s.pause = not s.pause
                s.show_pause_menu = not s.show_pause_menu
                s.logger.info("Gra wstrzymana" if s.pause else "Gra wznowiona")
                continue

            # ─── PAUSE-MENU BUTTONS ──────────────────────────────────
            if (s.show_pause_menu
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1):
                for btn in s.pause_menu_buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["text"] == "MENU":
                            return "menu"
                        if btn["text"] == "RESTART":
                            s.logger.info("Restart gry")
                            return "restart"
                        if btn["text"] == "SAVE":
                            snap = {
                                "tick": s.timer,
                                "save_decision": "player",
                                "turn": s.current_player(),
                                "cells": s.cells,
                            }
                            s.history.append(snap)
                            GameSaver(s.history)
                            s.logger.info("Zapisano grę")
                continue

            # ─── TERAZ WSZYSTKO PONIŻEJ TYLKO NA TWOJEJ TURZE ────────
            if current_owner != "player" or s.game_over or not s.player_turn:
                continue

            # ─── CONTEXT-MENU REMOVE (LPM) ──────────────────────────
            if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and s.context_menu_visible):
                x, y = s.context_menu_pos
                h = s.context_font.get_height() + 8
                for idx, target in enumerate(s.context_cell.connections):
                    rect = pygame.Rect(x, y + idx * h, 220, h)
                    if rect.collidepoint(event.pos):
                        s.logger.info(f"Usunięto połączenie z ({target.x}, {target.y})")
                        # s.context_cell.connections.remove(target)
                        for anim in s.animating_connections:
                            if anim.attacking_cell == s.context_cell and anim.attacked_cell == target:
                                anim.mark_for_removal = True
                        s.context_menu_visible = False
                        break
                continue

            # ─── LEFT-CLICK DOWN: wybór komórki ─────────────────────
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for cell in s.cells:
                    if (cell.is_in_area(event.pos, s.offset)
                        and cell.owner == "player"
                        and cell.owner_id == current_owner_id):
                        s.selected = cell
                        s.dragging = True
                        s.logger.info("Zaznaczono komórkę")
                        break
                continue

            # ─── LEFT-CLICK UP: zakończ łączenie ────────────────────
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if s.dragging and s.selected:
                    for cell in s.cells:
                        if (cell.is_in_area(event.pos, s.offset)
                            and cell != s.selected
                            and cell not in s.selected.connections):
                            limit = 3 if s.selected.type == "hex" else 2
                            if len(s.selected.connections) < limit:
                                s.animating_connections.append(
                                    AnimatedConnection(s.selected, cell)
                                )
                                s.logger.info("Połączono komórki")
                            else:
                                s.logger.info("Osiągnięto limit połączeń")
                            break
                s.selected = None
                s.dragging = False
                continue

            # ─── TOGGLE SUGGESTIONS (Spacja) ────────────────────────
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                s.suggestion_handler.toggle()
                continue

        # nie zmieniamy sceny
        return None
