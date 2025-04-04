from animated_connection import AnimatedConnection

class AI:
    def __init__(self):
        pass

    def generate_suggestion(self, cells):
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

                distance = ((source.x - target.x)**2 + (source.y - target.y)**2)**0.5
                score = (10 - target.units) - (distance / 100)

                if source.type == "attack":
                    score += 5
                if target.owner == "enemy":
                    score += 3

                if score > best_score:
                    best_score = score
                    best_move = (source, target)

        return best_move

    def enemy_turn(self, cells, animating_connections):
        enemy_cells = [c for c in cells if c.owner == 'enemy' and c.units > 5]
        potential_targets = [c for c in cells if c.owner != 'enemy']

        for source in enemy_cells:
            max_conns = 3 if source.type == "hex" else 2
            if len(source.connections) >= max_conns:
                continue

            best_score = float('-inf')
            best_target = None
            for target in potential_targets:
                if target in source.connections:
                    continue
                distance = ((source.x - target.x)**2 + (source.y - target.y)**2)**0.5
                score = (10 - target.units) - (distance / 100)
                if target.owner == 'player':
                    score += 2
                if score > best_score:
                    best_score = score
                    best_target = target

            if best_target:
                animating_connections.append(AnimatedConnection(source, best_target))
                source.connections.append(best_target)
