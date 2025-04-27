import pygame
import colors

class UIRenderer:
    def __init__(self, font, load_font, context_font, title_font, logger, manager=None):
        # fonts and optional GUI manager
        self.font = font
        self.load_font = load_font
        self.context_font = context_font
        self.title_font = title_font
        self.logger = logger
        # mapping of cell colors to names for status text
        self.color_names = {
            colors.GREEN: "Green",
            colors.RED: "Red",
            colors.PINK: "Pink",
            colors.ORANGE: "Orange",
            colors.GRAY: "Gray",
        }

    def draw(self, scene, screen):
        # Draw UI overlay: buttons, turn bar, status, suggestions, context menu, logs
        # 1. Draw main pause button and pause menu
        self._draw_button(screen, scene.main_button)
        if scene.show_pause_menu:
            for btn in scene.pause_menu_buttons:
                self._draw_button(screen, btn)

        # 2. Draw turn timer bar
        self._draw_turn_bar(scene, screen)

        # 3. Draw status text
        self._draw_status(scene, screen)

        # 4. Draw suggestion line if active
        self._draw_suggestion(scene, screen)

        # 5. Draw context menu when visible
        if scene.context_menu_visible and scene.context_cell:
            self._draw_context_menu(scene, screen)

        # 6. Draw logs in corner
        self._draw_logs(scene, screen)

    def _draw_button(self, screen, btn):
        mouse_pos = pygame.mouse.get_pos()
        hovered = btn["rect"].collidepoint(mouse_pos)
        base_color = (70, 70, 200)
        hover_color = (100, 100, 255)
        color = hover_color if hovered else base_color
        pygame.draw.rect(screen, color, btn["rect"], border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255), btn["rect"], 2, border_radius=6)
        text_surf = self.font.render(btn["text"], True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=btn["rect"].center)
        screen.blit(text_surf, text_rect)

    def _draw_turn_bar(self, scene, screen):
        # Draw the turn progress bar outline and background
        pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)
        pygame.draw.rect(screen, (200, 200, 200), (20, 60, 200, 10))

        # Determine bar color based on a representative cell of the current player
        owner, owner_id = scene.current_player()
        bar_color = colors.WHITE
        # find first cell belonging to this player/AI
        for cell in scene.cells:
            if cell.owner == owner and cell.owner_id == owner_id:
                bar_color = cell.color
                break

        # Fill current progress
        bar_w = int((scene.timer % scene.round_duration) / scene.round_duration * 200)
        pygame.draw.rect(screen, bar_color, (20, 60, bar_w, 10))

    def _draw_status(self, scene, screen):
        # Determine status text based on game over or current turn
        if scene.game_over:
            # End-of-game display
            if scene.winner:
                who, idx = scene.winner
                # Find representative cell to get its color name
                color_name = ''
                for cell in scene.cells:
                    if cell.owner == who and cell.owner_id == idx:
                        color_name = self.color_names.get(cell.color, '')
                        break
                text = f"{who.capitalize()}{color_name}wins!"
            else:
                text = 'DRAW'
        else:
            owner, owner_id = scene.current_player()
            # Find a cell of the current player to get its color
            color_name = ''
            for cell in scene.cells:
                if cell.owner == owner and cell.owner_id == owner_id:
                    color_name = self.color_names.get(cell.color, '')
                    break
            text = f"{color_name} {owner.capitalize()}'s turn"
        surf = self.font.render(text, True, colors.WHITE)
        screen.blit(surf, (20, 20))

    def _draw_suggestion(self, scene, screen):
        if scene.suggestion_handler.show and scene.suggestion_handler.suggestion:
            src, tgt = scene.suggestion_handler.suggestion
            ox, oy = scene.offset
            start = (src.x + ox, src.y + oy)
            end = (tgt.x + ox, tgt.y + oy)
            pygame.draw.line(screen, (0, 255, 255), start, end, 3)
            tip = self.font.render("Sugerowany ruch", True, (0, 255, 255))
            screen.blit(tip, (20, 90))

    def _draw_context_menu(self, scene, screen):
        x, y = scene.context_menu_pos
        w, h, pad, r = 220, 36, 8, 8
        for i, target in enumerate(scene.context_cell.connections):
            rect = pygame.Rect(x, y + i * (h + pad), w, h)
            shadow = rect.move(2, 2)
            pygame.draw.rect(screen, (0,0,0,100), shadow, border_radius=r)
            pygame.draw.rect(screen, (40,40,40), rect, border_radius=r)
            pygame.draw.rect(screen, (120,120,120), rect, 1, border_radius=r)
            label = f"{i+1}. Usuń połączenie z ({target.x}, {target.y})"
            surf = self.context_font.render(label, True, (240,240,240))
            sr = surf.get_rect(center=rect.center)
            screen.blit(surf, sr)

    def _draw_logs(self, scene, screen):
        lines = scene.log_handler.get_logs()
        x = 10
        y = screen.get_height() - 20 * len(lines) - 10
        for line in lines:
            surf = self.context_font.render(line, True, (255,255,0))
            screen.blit(surf, (x, y))
            y += 20
