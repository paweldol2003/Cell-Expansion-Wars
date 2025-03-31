# game_scene.py
import pygame
import sys
from cell import Cell
from animated_connection import AnimatedConnection
import colors
from enemyAI import EnemyAI
from logger import setup_logger


class GameScene:
    def __init__(self, cells, images):
        self.cells = cells
        self.images = images
        self.selected = None
        self.dragging = False
        self.mouse_pos = (0, 0)
        self.timer = 0
        self.animating_connections = []
        self.animated_bullets = []
        self.potential_connections = []
        self.context_cell = None  # komórka, na której otwarto menu
        self.context_menu_pos = None  # gdzie wyświetlić menu
        self.context_menu_visible = False

        self.enemy_ai = EnemyAI()
        self.suggestion = None  # (source_cell, target_cell)

        self.buttons = [
            {"text": "MENU", "rect": pygame.Rect(700, 20, 80, 30)},
        ]
        self.font = pygame.font.SysFont(None, 30)
        self.context_font = pygame.font.SysFont("consolas", 10)
        self.logger, self.log_handler = setup_logger()
        self.font_log = pygame.font.SysFont("consolas", 16)
        # Przesuwanie
        self.offset = [0, 0]         # globalne przesunięcie planszy
        self.is_panning = False      # flaga aktywnego przesuwania
        self.pan_start = (0, 0)
        self.selection_timer = 0  # do animacji pulsowania

        # System rund
        self.round_timer = 0
        self.round_duration = 4 * 60  # 4 sekund w klatkach (zakładając 60 FPS)
        self.player_turn = True  # True = gracz, False = AI

        # Stan gry
        self.game_over = False
        self.player_won = False

    def generate_suggestion(self):
        player_cells = [c for c in self.cells if c.owner == 'player' and c.units > 5]
        potential_targets = [c for c in self.cells if c.owner != 'player']

        best_score = float('-inf')
        best_move = None

        for source in player_cells:
            max_conns = 3 if source.type == "hex" else 2
            if len(source.connections) >= max_conns:
                continue

            for target in potential_targets:
                if target in source.connections:
                    continue

                # Prosta heurystyka: opłaca się atakować słabych i bliskich
                distance = ((source.x - target.x)**2 + (source.y - target.y)**2)**0.5
                score = (10 - target.units) - (distance / 100)

                if source.type == "attack":
                    score += 5
                if target.owner == "enemy":
                    score += 3

                if score > best_score:
                    best_score = score
                    best_move = (source, target)

        self.suggestion = best_move


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                self.suggestion = None
                if event.button == 3:  # PPM
                    for cell in self.cells:
                        if cell.is_in_area(event.pos, offset=self.offset):  # dodaj offset!
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
                    if btn["rect"].collidepoint(event.pos):
                        return 1

                if not self.player_turn or self.game_over:
                    return

                for cell in self.cells:
                    if cell.is_in_area(event.pos, self.offset) and cell.owner == 'player':
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

    def update(self):
        if self.game_over:
            return

        self.timer += 1
        self.round_timer += 1
        self.selection_timer += 1


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
        if self.round_timer == 1 and self.player_turn:
            self.generate_suggestion()

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

        self.animating_connections = [
            anim for anim in self.animating_connections if not getattr(anim, "to_destroy", False)
        ]


    def draw(self, screen: pygame.Surface):
        screen.fill(colors.GRAY)

        # Rysowanie animowanych połączeń
        for anim in self.animating_connections:
            anim.draw(screen, offset=self.offset)

        # Rysowanie linii przeciągania (jeśli zaznaczono komórkę)
        if self.dragging and self.selected:
            pygame.draw.line(screen, colors.GREEN,
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
        bar_width = int((self.round_timer / self.round_duration) * 200)
        pygame.draw.rect(screen, (200, 200, 200), (20, 60, 200, 10))  # tło paska
        if self.player_turn:
            pygame.draw.rect(screen, colors.GREEN, (20, 60, bar_width, 10))
        else:
            pygame.draw.rect(screen, colors.RED, (20, 60, bar_width, 10))

        # Informacja o stanie gry
        if self.game_over:
            pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)
            result_text = "YOU WON" if self.player_won else "YOU LOST"
            info = self.font.render(result_text, True, colors.WHITE)
            screen.blit(info, (400, 60))
        else:
            status_text = "Your turn" if self.player_turn else "AI turn"
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
                        pulse_radius = cell.radius + 4 + (self.selection_timer % 50) // 3
                        alpha = max(0, 255 - (self.selection_timer % 50) * 4)
                    else:
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
                    pulse_radius = cell.radius + 4 + (self.selection_timer % 100) // 3
                    alpha = max(0, 255 - (self.selection_timer % 100) * 4)

                    ring_surface = pygame.Surface((pulse_radius * 2 + 4, pulse_radius * 2 + 4), pygame.SRCALPHA)
                    pygame.draw.circle(
                        ring_surface,
                        (255, 255, 0, alpha),
                        (pulse_radius + 2, pulse_radius + 2),
                        pulse_radius,
                        3
                    )

                    screen.blit(ring_surface, (cx - pulse_radius - 2, cy - pulse_radius - 2))

            # Dodatkowe obramowanie na samej zaznaczonej komórce
            sel_x = self.selected.x + ox
            sel_y = self.selected.y + oy
            pygame.draw.circle(screen, (255, 255, 0), (sel_x, sel_y), self.selected.radius + 6, 4)

        if self.context_menu_visible and self.context_cell:
            x, y = self.context_menu_pos
            for idx, target in enumerate(self.context_cell.connections):
                rect = pygame.Rect(x, y + idx * 40, 220, 36)

                # Tło z przezroczystością
                button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                button_surf.fill((0, 0, 0, 0))  # przezroczyste tło

                # Zaokrąglony przycisk (ciemnoszary, półprzezroczysty)
                pygame.draw.rect(button_surf, (30, 30, 30, 220), button_surf.get_rect(), border_radius=8)

                # Obrys (jaśniejszy szary)
                pygame.draw.rect(button_surf, (100, 100, 100, 255), button_surf.get_rect(), width=1, border_radius=8)

                # Tekst
                text = self.context_font.render(f"🗑 Usuń połączenie z ({target.x}, {target.y})", True, (240, 240, 240))
                button_surf.blit(text, (10, 7))

                # Narysuj gotowy przycisk na ekran
                screen.blit(button_surf, rect.topleft)

        if self.suggestion:
            src, tgt = self.suggestion
            src_pos = (src.x + self.offset[0], src.y + self.offset[1])
            tgt_pos = (tgt.x + self.offset[0], tgt.y + self.offset[1])
            pygame.draw.line(screen, (0, 255, 255), src_pos, tgt_pos, 3)

            # Tekst
            tip_text = self.font.render("💡 Sugerowany ruch", True, (0, 255, 255))
            screen.blit(tip_text, (20, 90))

        

        for line in log_lines:
            rendered = self.font_log.render(line, True, (255, 255, 0))
            screen.blit(rendered, (log_x, log_y))
            log_y += 20


