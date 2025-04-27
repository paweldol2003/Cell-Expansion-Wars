# stages.py
from cell import Cell
import colors

# ───────────────────────── Istniejące poziomy ───────────────────────── #
def get_stage_1(images):
    r = 40
    return [
        Cell(0, 200, 300, r, colors.GREEN, "player", 1, "normal",  image_map=images),
        Cell(1, 600, 300, r, colors.RED,   "enemy",  1, "normal",  image_map=images),
    ]


def get_stage_2(images):
    r = 30
    return [
        # Gracz
        Cell(0, 100, 500, r, colors.GREEN, "player", 1, "normal",  image_map=images),

        # Wróg
        Cell(1, 700, 100, r, colors.RED,   "enemy",  1, "normal",  image_map=images),

        # Neutralne ─ każdy w innym stanie
        Cell(2, 400, 300, r, colors.GRAY, "neutral", 1, "hex",     image_map=images),
        Cell(3, 150, 150, r, colors.GRAY, "neutral", 1, "attack",  image_map=images),
        Cell(4, 650, 450, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(5, 400, 100, r, colors.GRAY, "neutral", 1, "normal",  image_map=images),
        Cell(6, 400, 500, r, colors.GRAY, "neutral", 1, "attack",  image_map=images),
        Cell(7, 100, 300, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(8, 700, 300, r, colors.GRAY, "neutral", 1, "hex",     image_map=images),
    ]


def get_stage_3(images):
    r = 40
    return [
        # Gracz
        Cell(0, 100, 500, r, colors.GREEN, "player", 1, "normal",  image_map=images),
        Cell(1, 150, 350, r, colors.GREEN, "player", 1, "attack",  image_map=images),

        # Wróg
        Cell(2, 700, 100, r, colors.RED,   "enemy",  1, "normal",  image_map=images),
        Cell(3, 650, 250, r, colors.RED,   "enemy",  1, "defence", image_map=images),

        # Neutralne
        Cell(4, 400, 300, r, colors.GRAY, "neutral", 1, "hex",     image_map=images),
        Cell(5, 300, 150, r, colors.GRAY, "neutral", 1, "normal",  image_map=images),
        Cell(6, 500, 450, r, colors.GRAY, "neutral", 1, "attack",  image_map=images),
        Cell(7, 400, 100, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
    ]


def get_stage_4(images):
    r = 40  # ← stały promień dla wszystkich komórek
    return [
        # Gracz
        Cell(0, 100, 550, r, colors.GREEN, "player", 1, "normal",  image_map=images),

        # Wróg
        Cell(1, 700,  50, r, colors.RED,   "enemy",  1, "normal",  image_map=images),

        # Neutralny „boss” + satelity
        Cell(2, 400, 300, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(3, 300, 250, r, colors.GRAY, "neutral", 1, "normal",  image_map=images),
        Cell(4, 500, 350, r, colors.GRAY, "neutral", 1, "attack",  image_map=images),
        Cell(5, 300, 350, r, colors.GRAY, "neutral", 1, "hex",     image_map=images),
        Cell(6, 500, 250, r, colors.GRAY, "neutral", 1, "normal",  image_map=images),
    ]


def get_stage_5(images):
    r = 35
    return [
        # Gracz
        Cell(0, 100, 300, r, colors.GREEN, "player", 1, "attack",  image_map=images),

        # Wrogowie
        Cell(1, 700, 100, r, colors.RED,   "enemy",  1, "normal",  image_map=images),
        Cell(2, 700, 500, r, colors.ORANGE,  "enemy",  2, "normal",  image_map=images),

        # Neutralne „wieże”
        Cell(3, 400, 100, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(4, 400, 500, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(5, 400, 300, r, colors.GRAY, "neutral", 1, "hex",     image_map=images),
    ]


def get_stage_6(images):
    r = 35  # ← wspólny promień
    return [
        # Gracz
        Cell(0, 100, 550, r, colors.GREEN, "player", 1, "normal",  image_map=images),

        # AI 1
        Cell(1, 700, 550, r, colors.RED,   "enemy",  1, "normal",  image_map=images),

        # AI 2
        Cell(2, 700,  50, r, colors.ORANGE,  "enemy",  2, "normal",  image_map=images),

        # Neutralne punkty kontrolne
        *[
            Cell(10 + i, x, y, r, colors.GRAY, "neutral", 1, "normal", image_map=images)
            for i, (x, y) in enumerate(
                [
                    (200, 100), (250, 200), (150, 400), (250, 500),
                    (400, 200), (400, 400),
                    (550, 100), (600, 200), (650, 300), (600, 400),
                ]
            )
        ],
    ]



def get_stage_3_multi(images):
    """Ta plansza zostaje bez zmian – tryb wieloosobowy."""
    r = 40
    return [
        # Gracz 1
        Cell(0, 100, 500, r, colors.GREEN, "player", 1, "normal",  image_map=images),
        Cell(1, 150, 350, r, colors.GREEN, "player", 1, "attack",  image_map=images),

        # Gracz 2 / AI
        Cell(2, 700, 100, r, colors.ORANGE,  "player", 2, "normal",  image_map=images),
        Cell(3, 650, 250, r, colors.ORANGE,  "player", 2, "attack",  image_map=images),

        # Neutralne
        Cell(4, 400, 300, r, colors.GRAY, "neutral", 1, "hex",     image_map=images),
        Cell(5, 300, 150, r, colors.GRAY, "neutral", 1, "normal",  image_map=images),
        Cell(6, 500, 450, r, colors.GRAY, "neutral", 1, "attack",  image_map=images),
        Cell(7, 400, 100, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
    ]
