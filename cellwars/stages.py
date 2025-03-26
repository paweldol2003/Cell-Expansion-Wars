# stages.py
from cell import Cell

BLUE = (100, 149, 237)
RED = (220, 20, 60)

def get_stage_1():
    return [
        Cell(200, 300, 40, BLUE, "player", "normal"),
        Cell(600, 300, 40, RED, "enemy", "normal")
    ]

def get_stage_2():
    return [
        Cell(200, 400, 40, BLUE, "player", "normal"),
        Cell(600, 200, 40, RED, "enemy", "normal")
    ]