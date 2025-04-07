import json
import xml.etree.ElementTree as ET
from pymongo import MongoClient

class GameSaver:
    def __init__(self, history, base_filename="game_history"):
        self.history = history
        self.base_filename = base_filename

        self.save_json()
        self.save_xml()
        self.save_mongo()

    def serialize_cell(self, cell):
        return {
            "id": cell.id,
            "x": cell.x,
            "y": cell.y,
            "radius": cell.radius,
            "color": cell.color,
            "owner": cell.owner,
            "owner_id": cell.owner_id,
            "units": cell.units,
            "type": cell.type,
            "connections": [c.id for c in cell.connections]
        }

    def save_json(self):
        try:
            json_data = []
            for entry in self.history:
                owner, owner_id = entry.get("turn", ("unknown", -1))
                json_data.append({
                    "tick": entry["tick"],
                    "turn": {
                        "owner": owner,
                        "owner_id": owner_id
                    },
                    "save_decision": entry.get("save_decision", "system"),
                    "cells": [self.serialize_cell(cell) for cell in entry["cells"]]
                })

            with open(f"{self.base_filename}.json", "w") as f:
                json.dump(json_data, f, indent=4)

        except Exception as e:
            print(f"Błąd zapisu JSON: {e}")

    def save_xml(self):
        try:
            root = ET.Element("game_history")

            for entry in self.history:
                owner, owner_id = entry.get("turn", ("unknown", -1))
                tick_elem = ET.SubElement(root, "tick", attrib={
                    "value": str(entry["tick"]),
                    "owner": str(owner),
                    "owner_id": str(owner_id),
                    "save_decision": entry.get("save_decision", "system")
                })

                for cell in entry["cells"]:
                    cell_elem = ET.SubElement(tick_elem, "cell", attrib={
                        "id": str(cell.id),
                        "x": str(cell.x),
                        "y": str(cell.y),
                        "radius": str(cell.radius),
                        "color": str(cell.color),
                        "owner": cell.owner,
                        "owner_id": str(cell.owner_id),
                        "units": str(cell.units),
                        "type": cell.type,
                    })

                    for conn in cell.connections:
                        ET.SubElement(cell_elem, "connection", attrib={"id": str(conn.id)})

            tree = ET.ElementTree(root)
            tree.write(f"{self.base_filename}.xml", encoding="utf-8", xml_declaration=True)

        except Exception as e:
            print(f"Błąd zapisu XML: {e}")

    def save_mongo(self):
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["cellwars"]
            collection = db["history"]
            collection.delete_many({})

            formatted = []
            for entry in self.history:
                owner, owner_id = entry.get("turn", ("unknown", -1))
                formatted.append({
                    "tick": entry["tick"],
                    "turn": {
                        "owner": owner,
                        "owner_id": owner_id
                    },
                    "save_decision": entry.get("save_decision", "system"),
                    "cells": [self.serialize_cell(cell) for cell in entry["cells"]]
                })

            collection.insert_many(formatted)

        except Exception as e:
            print(f"Błąd zapisu do MongoDB: {e}")
