from cell import Cell
import colors

def get_stage_1(images):
    r = 40
    return [
        Cell(0, 200, 300, r, colors.GREEN, "player", 1, "normal", image_map=images),
        Cell(1, 600, 300, r, colors.RED, "enemy", 1, "normal", image_map=images),
    ]

def get_stage_2(images):
    r = 30  # bazowy promień
    return [
        # Gracz
        Cell(0, 100, 500, r, colors.GREEN, "player", 1, "normal", image_map=images),

        # Wróg
        Cell(1, 700, 100, r, colors.RED, "enemy", 1, "normal", image_map=images),

        # Neutralne ─ każdy w innym stanie
        Cell(2, 400, 300, r, colors.GRAY, "neutral", 1, "hex", image_map=images),
        Cell(3, 150, 150, r, colors.GRAY, "neutral", 1, "attack", image_map=images),
        Cell(4, 650, 450, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(5, 400, 100, r, colors.GRAY, "neutral", 1, "normal", image_map=images),
        Cell(6, 400, 500, r, colors.GRAY, "neutral", 1, "attack", image_map=images),
        Cell(7, 100, 300, r, colors.GRAY, "neutral", 1, "defence", image_map=images),
        Cell(8, 700, 300, r, colors.GRAY, "neutral", 1, "hex", image_map=images),
    ]

def get_stage_3(images):
    r = 40
    return [
        # Gracz
        Cell(0, 100, 500, r, colors.GREEN, "player", 1, "normal", image_map=images),
        Cell(1, 150, 350, r, colors.GREEN, "player", 1, "attack", image_map=images),

        # Wróg
        Cell(2, 700, 100, r, colors.RED, "enemy", 1, "normal", image_map=images),
        Cell(3, 650, 250, r, colors.RED, "enemy", 1, "defence", image_map=images),

        # Neutralne
        Cell(4, 400, 300, r, colors.GRAY, "neutral", 1,  "hex", image_map=images),
        Cell(5, 300, 150, r, colors.GRAY, "neutral", 1,  "normal", image_map=images),
        Cell(6, 500, 450, r, colors.GRAY, "neutral", 1,  "attack", image_map=images),
        Cell(7, 400, 100, r, colors.GRAY, "neutral", 1,  "defence", image_map=images),
    ]

def get_stage_3_multi(images):
    r = 40
    return [
        # Gracz 1
        Cell(0, 100, 500, r, colors.GREEN, "player", 1, "normal", image_map=images),
        Cell(1, 150, 350, r, colors.GREEN, "player", 1, "attack", image_map=images),

        # Gracz 2 lub AI
        Cell(2, 700, 100, r, colors.PINK, "player", 2, "normal", image_map=images),
        Cell(3, 650, 250, r, colors.PINK, "player", 2, "attack", image_map=images),

        # Neutralne
        Cell(4, 400, 300, r, colors.GRAY, "neutral", 1,  "hex", image_map=images),
        Cell(5, 300, 150, r, colors.GRAY, "neutral", 1,  "normal", image_map=images),
        Cell(6, 500, 450, r, colors.GRAY, "neutral", 1,  "attack", image_map=images),
        Cell(7, 400, 100, r, colors.GRAY, "neutral", 1,  "defence", image_map=images),
    ]
