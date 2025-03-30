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

        enemy_cells_ready_to_attack = [c for c in cells if c.owner == "enemy" and c.units >= 20]

        for cell in enemy_cells_ready_to_attack:
            # wybierz losowy cel: neutralny lub gracza
            potential_targets = [
                target for target in cells
                if target.owner != "enemy"
            ]

            if potential_targets:
                target = random.choice(potential_targets)
                units_to_send = cell.units // 2
                cell.units -= units_to_send

                anim = AnimatedConnection(cell, target)
                anim.bullets_to_fire = units_to_send
                anim.mark_for_removal = True  # nowy flag
                animating_connections.append(anim)

                if target in cell.connections:
                    cell.connections.remove(target)


                
