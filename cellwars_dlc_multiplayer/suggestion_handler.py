# suggestion_handler.py

class SuggestionHandler:
    def __init__(self):
        self.show = False
        self.suggestion = None

    def toggle(self):
        self.show = not self.show

    def set_suggestion(self, suggestion):
        self.suggestion = suggestion

    def reset(self):
        self.suggestion = None
        self.show = False

    def generate(self, cells):
        player_cells = [c for c in cells if c.owner == 'player' and c.units > 5]
        potential_targets = [c for c in cells if c.owner != 'player']

        best_score = float('-inf')
        best_move = None

        for source in player_cells:
            max_conns = 3 if source.type == "hex" else 2
            if len(source.connections) >= max_conns:
                continue

            for target in potential_targets:
                if target in source.connections:
                    continue

                # Heurystyka: słaby i bliski cel
                distance = ((source.x - target.x) ** 2 + (source.y - target.y) ** 2) ** 0.5
                score = (10 - target.units) - (distance / 100)

                if source.type == "attack":
                    score += 5
                if target.owner == "enemy":
                    score += 3

                if score > best_score:
                    best_score = score
                    best_move = (source, target)

        self.set_suggestion(best_move)
