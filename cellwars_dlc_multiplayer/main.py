# main.py
import pygame
import pygame_gui

import stages
from scenes import GameScene, MenuScene
from assets.resources import load_images
from game_loader import GameLoader
from animated_connection import AnimatedConnection


# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Expansion Wars")
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

images = load_images()


# Główna pętla gry
def main():
    clock = pygame.time.Clock()
    current_scene = "menu"
    menu = MenuScene(images, WINDOW, manager)
    game = None
    cells = []
    actual_stage = None

    while True:
        clock.tick(60)
        events = pygame.event.get()

        if current_scene == "menu":
            result = menu.handle_events(events)
            actual_stage = result
            if result:
                # ─── obsługa nowych poziomów 1–6 ─────────────────
                if result == "stage_1":
                    cells = stages.get_stage_1(images)
                elif result == "stage_2":
                    cells = stages.get_stage_2(images)
                elif result == "stage_3":
                    cells = stages.get_stage_3(images)
                elif result == "stage_4":
                    cells = stages.get_stage_4(images)
                elif result == "stage_5":
                    cells = stages.get_stage_5(images)
                elif result == "stage_6":
                    cells = stages.get_stage_6(images)
                # ──────────────────────────────────────────────────
                elif result == "stage_3_multi":
                    cells = stages.get_stage_3_multi(images)
                elif result in ("load_json", "load_xml", "load_mongo"):
                    loader = GameLoader(image_map=images)

                    if result == "load_json":
                        loaded_data = loader.load_from_json()
                    elif result == "load_xml":
                        loaded_data = loader.load_from_xml()
                    elif result == "load_mongo":
                        loaded_data = loader.load_from_mongo()

                    cells = loaded_data["cells"]
                    game = GameScene(cells, images)
                    # Odtwórz animacje połączeń na podstawie logicznych connections
                    for cell in game.cells:
                        for target in cell.connections:
                            # Tylko jednostronne, by nie dublować
                            if not any(
                                anim.start_cell == cell and anim.end_cell == target
                                for anim in game.animating_connections
                            ):
                                game.animating_connections.append(
                                    AnimatedConnection(cell, target, speed=1.0)
                                )  # speed=1.0 = natychmiast kończy animację

                    current_turn = loaded_data["turn"]
                    game.turn_order = game.compute_turn_order()  # <- TO JEST KLUCZOWE
                    game.current_turn_index = game.turn_order.index(current_turn)
                    game.timer = loaded_data["timer"]

                    current_scene = "game"
                    continue  # od razu przejdź do aktualizacji gry w tej samej pętli
                else:
                    cells = []

                # start nowej gry na wybranym etapie
                game = GameScene(cells, images)
                current_scene = "game"

            # rysuj menu
            menu.update(clock.get_time() / 1000)
            menu.draw(WINDOW)

        elif current_scene == "game":
            result = game.handle_events(events)
            if result == "menu":
                menu = MenuScene(images, WINDOW, manager)
                current_scene = "menu"
            elif result == "restart":
                # restart bieżącej planszy
                game = GameScene(cells, images)
            else:
                game.update()
                game.draw(WINDOW)

        pygame.display.flip()


if __name__ == "__main__":
    main()
