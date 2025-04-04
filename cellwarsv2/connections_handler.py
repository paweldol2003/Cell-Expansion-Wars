from animated_connection import AnimatedConnection

class ConnectionHandler:
    def __init__(self):
        self.animating_connections = []

    def add_connection(self, source_cell, target_cell):
        # Dodaj animację
        animation = AnimatedConnection(source_cell, target_cell)
        self.animating_connections.append(animation)

        # Dodaj połączenie logiczne
        source_cell.connections.append(target_cell)

    def update_connections(self, timer):
        shoot_now = (timer == 50)
        for anim in self.animating_connections:
            anim.update(shoot=shoot_now)

        # Usuń animacje oznaczone do usunięcia
        self.animating_connections = [
            anim for anim in self.animating_connections if not getattr(anim, "to_destroy", False)
        ]
