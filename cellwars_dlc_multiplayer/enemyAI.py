# enemyAI.py
import heapq
from math import hypot
from collections import defaultdict
from animated_connection import AnimatedConnection

class EnemyAI:
    """
    Utility‐based AI z ograniczeniem connections:
      • typ != "hex" → max 2 połączenia
      • typ == "hex" → max 3 połączenia
    """

    def __init__(self,
                 min_units: int = 10,
                 cooldown: int = 180,
                 w_defensive:    float = 30.0,
                 w_support:      float = 1.0,
                 w_attack_enemy: float = 1.0,
                 w_attack_neutral: float = 0.5):
        self.min_units         = min_units
        self.cooldown          = cooldown
        self.w_defensive       = w_defensive
        self.w_support         = w_support
        self.w_attack_enemy    = w_attack_enemy
        self.w_attack_neutral  = w_attack_neutral

        # timery per owner_id
        self.timer = defaultdict(int)

    def update(self, owner_id: int, cells, animating_connections):
        # ─── cooldown ───────────────────────────────────────────────
        t = self.timer[owner_id] + 1
        if t < self.cooldown:
            self.timer[owner_id] = t
            return
        self.timer[owner_id] = 0

        # ─── wybór własnych komórek ─────────────────────────────────
        my_cells = [
            c for c in cells
            if c.owner == "enemy"
               and c.owner_id == owner_id
               and c.units >= self.min_units
        ]
        if not my_cells:
            return

        allies   = [c for c in cells if c.owner == "enemy" and c.owner_id == owner_id]
        enemies  = [c for c in cells if not (c.owner == "enemy" and c.owner_id == owner_id)]
        neutrals = [c for c in cells if c.owner == "neutral"]

        best_u = -float("inf")
        best_action = None  # (typ, attacker, target)

        for attacker in my_cells:
            # oblicz limit połączeń
            max_conns = 3 if attacker.type == "hex" else 2

            # 1) DefensiveCut – zawsze możliwe (usunięcie connections)
            under_attack = any(
                attacker in other.connections
                for other in cells
                if not (other.owner == "enemy" and other.owner_id == owner_id)
            )
            if under_attack:
                u = self.w_defensive * attacker.units
                if u > best_u:
                    best_u = u
                    best_action = ("defensive", attacker, None)

            # jeśli mamy już max connections, pomijamy support/attack
            if len(attacker.connections) >= max_conns:
                continue

            # 2) SupportAlly
            for ally in allies:
                if ally is attacker:
                    continue
                if (ally in attacker.connections or
                    attacker in ally.connections or
                    any(anim.attacking_cell or anim.attacked_cell is attacker and anim.attacked_cell or anim.attacked_cell is ally
                        for anim in animating_connections)):
                    continue
                dist = self._path_distance(attacker, ally)
                w_sup = self.w_support * (2 if attacker.type == "defence" else 1)

                u = w_sup * (ally.units / (dist + 1))
                if u > best_u:
                    best_u = u
                    best_action = ("support", attacker, ally)

            # 3) AttackEnemy
            for enemy in enemies:
                if (enemy in attacker.connections or
                    attacker in enemy.connections or
                    any(anim.attacking_cell is attacker and anim.attacked_cell is enemy
                        for anim in animating_connections)):
                    continue
                dist = self._path_distance(attacker, enemy)
                w_att = self.w_attack_enemy * (2 if attacker.type == "attack" else 1)
                u = w_att * ((attacker.units - enemy.units) / (dist + 1))
                if u > best_u:
                    best_u = u
                    best_action = ("attack_enemy", attacker, enemy)

            # 4) AttackNeutral
            for neutral in neutrals:
                if (neutral in attacker.connections or
                    attacker in neutral.connections or
                    any(anim.attacking_cell is attacker and anim.attacked_cell is neutral
                        for anim in animating_connections)):
                    continue
                dist = self._path_distance(attacker, neutral)
                w_att_n = self.w_attack_neutral * (2 if attacker.type == "attack" else 1)

                u = w_att_n * (neutral.units / (dist + 1))
                if u > best_u:
                    best_u = u
                    best_action = ("attack_neutral", attacker, neutral)

        # ─── wykonanie najlepszej akcji ─────────────────────────────
        if best_action:
            typ, atk, tgt = best_action
            if typ == "defensive":
                self.defensive_cut(atk, animating_connections)
            else:
                # przed dodaniem animacji jeszcze raz weryfikujemy max_conns
                max_conns = 3 if atk.type == "hex" else 2
                already = (tgt in atk.connections or atk in tgt.connections)
                pending = any(anim.attacking_cell is atk and anim.attacked_cell is tgt
                              for anim in animating_connections)
                if not already and not pending and len(atk.connections) < max_conns:
                    animating_connections.append(AnimatedConnection(atk, tgt))

    def defensive_cut(self, cell, animating_connections):
        """
        Usuń wszystkie logiczne połączenia tej komórki i oznacz animacje do usunięcia.
        """
        for nbr in cell.connections.copy():
            cell.connections.remove(nbr)
            if cell in nbr.connections:
                nbr.connections.remove(cell)
            for anim in animating_connections:
                if ((anim.attacking_cell is cell and anim.attacked_cell is nbr) or
                    (anim.attacking_cell is nbr and anim.attacked_cell is cell)):
                    anim.mark_for_removal = True

    def _path_distance(self, start, goal):
        """
        A* z heurystyką euklidesową. Zwraca koszt najkrótszej ścieżki
        przez istniejące połączenia, lub fallback na euklidesową.
        """
        h = lambda a, b: hypot(a.x - b.x, a.y - b.y)
        pq = [(h(start, goal), 0.0, start)]
        best_g = {start: 0.0}

        while pq:
            f, g, node = heapq.heappop(pq)
            if node is goal:
                return g
            if g > best_g[node]:
                continue
            for nbr in node.connections:
                w = hypot(node.x - nbr.x, node.y - nbr.y)
                ng = g + w
                if ng < best_g.get(nbr, float("inf")):
                    best_g[nbr] = ng
                    heapq.heappush(pq, (ng + h(nbr, goal), ng, nbr))

        # fallback, gdy brak ścieżki w grafie
        return hypot(start.x - goal.x, start.y - goal.y)
