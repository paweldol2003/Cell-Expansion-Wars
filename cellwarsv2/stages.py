# stages.py
from cell import Cell
import colors

def get_stage_1(images):
    r = 40
    return [
        Cell(200, 300, r, colors.BLUE, "player", "normal", image_map=images),
        Cell(600, 300, r, colors.RED, "enemy", "normal", image_map=images),
    ]

def get_stage_2(images):
    r = 40
    return [
        # Gracz – lewy dolny róg
        Cell(100, 500, r, colors.BLUE, "player", "normal", image_map=images),

        # Wróg – prawy górny róg
        Cell(700, 100, r, colors.RED, "enemy", "normal", image_map=images),

        # Neutralne komórki – strategiczne pozycje
        Cell(400, 300, r, colors.GRAY, "neutral", "normal", image_map=images),
        Cell(250, 200, r, colors.GRAY, "neutral", "normal", image_map=images),
        Cell(550, 400, r, colors.GRAY, "neutral", "normal", image_map=images),
    ]
def get_stage_3(images):
    r = 40
    return [
        # Gracz
        Cell(100, 500, r, colors.BLUE, "player", "normal", image_map=images),
        Cell(150, 350, r, colors.BLUE, "player", "attack", image_map=images),

        # Wróg
        Cell(700, 100, r, colors.RED, "enemy", "normal", image_map=images),
        Cell(650, 250, r, colors.RED, "enemy", "defence", image_map=images),

        # Neutralne
        Cell(400, 300, r, colors.GRAY, "neutral", "hex", image_map=images),
        Cell(300, 150, r, colors.GRAY, "neutral", "normal", image_map=images),
        Cell(500, 450, r, colors.GRAY, "neutral", "attack", image_map=images),
        Cell(400, 100, r, colors.GRAY, "neutral", "defence", image_map=images),
    ]
