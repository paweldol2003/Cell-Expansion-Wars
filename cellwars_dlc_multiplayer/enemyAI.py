import random
from animated_connection import AnimatedConnection

class EnemyAI:
    def __init__(self, attack_cooldown=120):
        self.timer = {}
        self.cooldown = attack_cooldown

    def update(self, owner_id, cells, animating_connections):
        # Ustawienie osobnego timera dla każdego przeciwnika
        if owner_id not in self.timer:
            self.timer[owner_id] = 0

        self.timer[owner_id] += 1
        if self.timer[owner_id] < self.cooldown:
            return

        self.timer[owner_id] = 0

        # Filtruj komórki tylko tego AI
        enemy_cells = [c for c in cells if c.owner == "enemy" and c.owner_id == owner_id and c.units >= 20]
        targets = [c for c in cells if not (c.owner == "enemy" and c.owner_id == owner_id)]

        for attacker in enemy_cells:
            if not targets:
                break

            max_conns = 3 if attacker.type == "hex" else 2
            if len(attacker.connections) >= max_conns:
                continue

            target = random.choice(targets)
            units_to_send = attacker.units // 2
            attacker.units -= units_to_send

            anim = AnimatedConnection(attacker, target)
            anim.bullets_to_fire = units_to_send
            animating_connections.append(anim)

            # Usuń połączenie jeśli istnieje (zabezpieczenie)
            try:
                attacker.connections.remove(target)
            except ValueError:
                pass
