# enemyAI.py
import heapq, random
from math import hypot
from collections import defaultdict
from animated_connection import AnimatedConnection


class EnemyAI:
    """
    • cel = units + weight * A*-distance (niższy = lepszy);
      neutralne komórki mają mnożnik neutral_factor (< 1 ⇒ priorytet).
    • jeśli moja komórka występuje w connections obcego gracza, usuwa
      wszystkie swoje połączenia (obrona).
    """

    def __init__(self,
                 attack_cooldown: int = 90,
                 min_units: int = 35,
                 weight: float = 5.0,
                 neutral_factor: float = 0.5):          # < 1 ⇒ neutralne „tańsze”
        self.cooldown = attack_cooldown
        self.min_units = min_units
        self.weight = weight
        self.neutral_factor = neutral_factor
        self.timer = defaultdict(int)

    # ------------------------------------------------------------------ #
    def update(self, owner_id: int, cells, animating_connections) -> None:
        # --- COOLDOWN -------------------------------------------------- #
        self.timer[owner_id] += 1
        if self.timer[owner_id] < self.cooldown:
            # nawet podczas cooldown-u sprawdzamy, czy coś nas nie atakuje
            self._defensive_cut(owner_id, cells, animating_connections)
            return
        self.timer[owner_id] = 0

        # --- PODZIAŁ KOMÓREK ------------------------------------------ #
        my_cells = [c for c in cells
                    if c.owner == "enemy" and c.owner_id == owner_id and c.units >= self.min_units]
        if not my_cells:
            return

        # najpierw obrona – odetnij połączenia, jeśli ktoś nas atakuje
        self._defensive_cut(owner_id, cells, animating_connections)

        targets = [c for c in cells
                   if not (c.owner == "enemy" and c.owner_id == owner_id)]

        # --- SORTUJ NAPASTNIKÓW --------------------------------------- #
        my_cells.sort(key=lambda c: c.units, reverse=True)

        # --- WYBÓR CELU ----------------------------------------------- #
        for attacker in my_cells:
            if self._has_max_connections(attacker):
                continue

            best_tgt, best_score = None, float("inf")
            for tgt in targets:
                if tgt in attacker.connections:
                    continue
                path_len = self._astar(attacker, tgt)
                if path_len is None:
                    continue

                score = tgt.units + self.weight * path_len
                if tgt.owner == "neutral":
                    score *= self.neutral_factor     # premiuj neutralne

                if score < best_score:
                    best_score, best_tgt = score, tgt

            if best_tgt:
                animating_connections.append(AnimatedConnection(attacker, best_tgt))
                break                                # jedno połączenie na cooldown

    # ------------------------------------------------------------------ #
    # -----------------------  POMOCNICZE  ------------------------------ #
    def _has_max_connections(self, cell):
        return len(cell.connections) >= (3 if cell.type == "hex" else 2)

    # ----------  A* po grafie połączeń  ----------
    def _astar(self, start, goal):
        h = lambda a, b: hypot(a.x - b.x, a.y - b.y)
        pq = [(h(start, goal), 0.0, start)]          # (f, g, node)
        best = {start: 0.0}
        while pq:
            f, g, node = heapq.heappop(pq)
            if node is goal:
                return g
            for n in node.connections:
                w = hypot(node.x - n.x, node.y - n.y)
                ng = g + w
                if ng < best.get(n, float("inf")):
                    best[n] = ng
                    heapq.heappush(pq, (ng + h(n, goal), ng, n))
        return None

    # ----------  Samoodcinanie się w obronie  ----------
    def _defensive_cut(self, owner_id, cells, animating_connections):
        """
        Jeśli komórka bota jest w connections obcego gracza,
        usuwa wszystkie swoje połączenia (i odpowiadające animacje).
        """
        # krok 1: zbierz moje komórki pod ostrzałem
        my_cells = [c for c in cells if c.owner == "enemy" and c.owner_id == owner_id]
        under_attack = [m for m in my_cells if any(
            (c.owner != "enemy" or c.owner_id != owner_id) and m in c.connections
            for c in cells)]
        if not under_attack:
            return

        # krok 2: zerwij ich połączenia
        for cell in under_attack:
            while cell.connections:                   # iterate copy
                tgt = cell.connections.pop()

                # usuń odpowiadające animacje (start==cell & end==tgt)
                for anim in animating_connections:
                    if anim.start_cell is cell and anim.end_cell is tgt:
                        anim.mark_for_removal = True
