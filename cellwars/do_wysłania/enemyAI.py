# enemyAI.py
import random
from animated_connection import AnimatedConnection

class EnemyAI:
    def __init__(self, attack_cooldown=120):
        self.timer = 0
        self.cooldown = attack_cooldown

    def update(self, cells, animating_connections):
        self.timer += 1
        if self.timer < self.cooldown:
            return
        self.timer = 0

        enemy_cells = [c for c in cells if c.owner == "enemy" and c.units >= 20]
        targets = [c for c in cells if c.owner != "enemy"]

        for attacker in enemy_cells:
            if not targets:
                break

            # LIMIT: 2 lub 3 połączenia
            max_conns = 3 if attacker.type == "hex" else 2
            if len(attacker.connections) >= max_conns:
                continue

            target = random.choice(targets)
            units_to_send = attacker.units // 2
            attacker.units -= units_to_send

            anim = AnimatedConnection(attacker, target)
            anim.bullets_to_fire = units_to_send
            # anim.mark_for_removal = True

            animating_connections.append(anim)

            # Usuń połączenie, jeśli istnieje (dla bezpieczeństwa)
            try:
                attacker.connections.remove(target)
            except ValueError:
                pass

