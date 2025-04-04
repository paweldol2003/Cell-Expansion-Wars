class GameLogic:
    def __init__(self):
        self.timer = 0
        self.round_timer = 0
        self.round_duration = 4 * 60  # 4 sekundy w klatkach (zakładamy 60 FPS)
        self.player_turn = True
        self.game_over = False
        self.player_won = False

    def update(self, cells):
        if self.game_over:
            return

        self.timer += 1
        self.round_timer += 1

        # Warunek zwycięstwa
        if not any(cell.owner == 'enemy' for cell in cells):
            self.game_over = True
            self.player_won = True
            return

        # Warunek przegranej
        if not any(cell.owner == 'player' for cell in cells):
            self.game_over = True
            self.player_won = False
            return

        # Zmiana rundy
        if self.round_timer >= self.round_duration:
            self.player_turn = not self.player_turn
            self.round_timer = 0
