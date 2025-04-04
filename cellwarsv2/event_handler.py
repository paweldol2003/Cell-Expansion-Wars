import pygame
from animated_connection import AnimatedConnection

class EventHandler:
    def __init__(self, cells, logger, connection_handler):
        self.cells = cells
        self.logger = logger
        self.connection_handler = connection_handler
        self.selected = None
        self.dragging = False
        self.is_panning = False
        self.pan_start = (0, 0)
        self.mouse_pos = (0, 0)

    def handle_events(self, event, game_scene):
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Obsługa kliknięcia przycisku MENU
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in game_scene.buttons:
                if btn["rect"].collidepoint(event.pos):
                    if btn["text"] == "MENU":
                        return "menu"

        # Pozostałe zdarzenia
        self.handle_event(event, game_scene)

        return None

    def handle_event(self, event, game_scene):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pos = event.pos
            game_scene.suggestion = None

            if event.button == 3:  # PPM
                for cell in self.cells:
                    if cell.is_in_area(event.pos, offset=game_scene.offset):
                        game_scene.context_cell = cell
                        game_scene.context_menu_pos = event.pos
                        game_scene.context_menu_visible = True
                        return
                game_scene.context_menu_visible = False
                self.is_panning = True
                self.pan_start = event.pos
                self.logger.info("Przesuwanie planszy")

            elif event.button == 1:
                if game_scene.context_menu_visible and game_scene.context_cell:
                    x, y = game_scene.context_menu_pos
                    for idx, target in enumerate(game_scene.context_cell.connections):
                        rect = pygame.Rect(x, y + idx * 30, 200, 30)
                        if rect.collidepoint(event.pos):
                            game_scene.context_cell.connections.remove(target)
                            self.logger.info(f"Usunięto połączenie z ({target.x}, {target.y})")
                            for anim in self.connection_handler.animating_connections:
                                if anim.start_cell == game_scene.context_cell and anim.end_cell == target:
                                    anim.mark_for_removal = True
                            game_scene.context_menu_visible = False
                            return
                    game_scene.context_menu_visible = False

                if not game_scene.game_logic.player_turn or game_scene.game_logic.game_over:
                    return

                for cell in self.cells:
                    if cell.is_in_area(event.pos, game_scene.offset) and cell.owner == 'player':
                        self.selected = cell
                        self.dragging = True
                        self.logger.info("Zaznaczono komórkę")
                        return

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.is_panning = False

            elif self.dragging and self.selected:
                for cell in self.cells:
                    if cell.is_in_area(event.pos, game_scene.offset):
                        if cell != self.selected and cell not in self.selected.connections:
                            max_conns = 3 if self.selected.type == "hex" else 2
                            if len(self.selected.connections) >= max_conns:
                                self.logger.info("Osiągnięto limit połączeń dla tej komórki.")
                                self.selected = None
                                break
                            self.connection_handler.add_connection(self.selected, cell)
                        break
                self.selected = None
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            if self.is_panning:
                dx = event.pos[0] - self.pan_start[0]
                dy = event.pos[1] - self.pan_start[1]
                game_scene.offset[0] += dx
                game_scene.offset[1] += dy
                self.pan_start = event.pos
