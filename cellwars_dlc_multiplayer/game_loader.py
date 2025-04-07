import json
from cell import Cell
import xml.etree.ElementTree as ET


class GameLoader:
    def __init__(self, filename="game_history.json", image_map=None):
        self.filename = filename
        self.image_map = image_map

    def load_from_json(self):
        with open(self.filename, "r") as f:
            data = json.load(f)

        last_state = data[-1]

        # Przywrócenie ogólnego stanu
        timer = last_state["tick"]
        turn_dict = last_state["turn"]
        current_turn = (turn_dict["owner"], turn_dict["owner_id"])


        save_decision = last_state["save_decision"]  # niekonieczne

        # Przywrócenie komórek
        raw_cells = last_state["cells"]
        id_to_cell = {}
        for raw in raw_cells:
            cell = Cell(
                id=raw["id"],
                x=raw["x"],
                y=raw["y"],
                radius=raw["radius"],
                color=tuple(raw["color"]),
                owner=raw["owner"],
                owner_id=raw["owner_id"],
                type=raw["type"],
                image_map=self.image_map
            )
            cell.units = raw["units"]
            id_to_cell[cell.id] = cell

        # Przywrócenie połączeń
        for raw in raw_cells:
            cell = id_to_cell[raw["id"]]
            cell.connections = [id_to_cell[conn_id] for conn_id in raw["connections"]]

        return {
            "cells": list(id_to_cell.values()),
            "timer": timer,
            "turn": current_turn
        }
    def load_from_xml(self, filename="game_history.xml"):
        tree = ET.parse(filename)
        root = tree.getroot()

        last_tick = root.findall("tick")[-1]
        timer = int(last_tick.attrib["value"])
        turn = (last_tick.attrib["owner"], int(last_tick.attrib["owner_id"]))

        id_to_cell = {}

        # Wczytaj komórki
        for cell_elem in last_tick.findall("cell"):
            cell = Cell(
                id=int(cell_elem.attrib["id"]),
                x=int(cell_elem.attrib["x"]),
                y=int(cell_elem.attrib["y"]),
                radius=int(cell_elem.attrib["radius"]),
                color=tuple(map(int, cell_elem.attrib["color"].strip("()").split(","))),
                owner=cell_elem.attrib["owner"],
                owner_id=int(cell_elem.attrib["owner_id"]),
                type=cell_elem.attrib["type"],
                image_map=self.image_map
            )
            cell.units = int(cell_elem.attrib["units"])
            id_to_cell[cell.id] = cell

        # Wczytaj połączenia
        for cell_elem in last_tick.findall("cell"):
            cell = id_to_cell[int(cell_elem.attrib["id"])]
            for conn in cell_elem.findall("connection"):
                conn_id = int(conn.attrib["id"])
                cell.connections.append(id_to_cell[conn_id])

        return {
            "cells": list(id_to_cell.values()),
            "timer": timer,
            "turn": turn
        }
