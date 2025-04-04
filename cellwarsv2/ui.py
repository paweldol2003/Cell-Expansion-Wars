import pygame
import colors

class UI:
    def __init__(self, font, log_handler):
        self.font = font
        self.log_handler = log_handler
        self.font_log = pygame.font.SysFont("consolas", 16)

    def draw_buttons(self, screen, buttons):
        for btn in buttons:
            pygame.draw.rect(screen, (70, 70, 200), btn["rect"])
            text = self.font.render(btn["text"], True, (255, 255, 255))
            screen.blit(text, (btn["rect"].x + 10, btn["rect"].y + 5))

    def draw_status(self, screen, game_over, player_won, player_turn):
        if game_over:
            result_text = "YOU WON" if player_won else "YOU LOST"
            info = self.font.render(result_text, True, colors.WHITE)
            screen.blit(info, (400, 60))
        else:
            status_text = "Your turn" if player_turn else "AI turn"
            info = self.font.render(status_text, True, colors.WHITE)
            screen.blit(info, (20, 20))

    def draw_logs(self, screen):
        log_lines = self.log_handler.get_logs()
        log_x = 10
        log_y = screen.get_height() - 20 * len(log_lines) - 10

        for line in log_lines:
            rendered = self.font_log.render(line, True, (255, 255, 0))
            screen.blit(rendered, (log_x, log_y))
            log_y += 20
    def draw_turn_bar(self, screen, round_timer, round_duration, player_turn):
        pygame.draw.rect(screen, colors.BLACK, (19, 59, 202, 12), 3)  # ramka
        bar_width = int((round_timer / round_duration) * 200)
        pygame.draw.rect(screen, (200, 200, 200), (20, 60, 200, 10))  # tło paska
        pygame.draw.rect(
            screen,
            colors.GREEN if player_turn else colors.RED,
            (20, 60, bar_width, 10)
        )