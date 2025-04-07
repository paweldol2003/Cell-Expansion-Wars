#main.py
import pygame
import stages
from scenes import GameScene, MenuScene
from assets.resources import load_images

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Expansion Wars")
images = load_images()


# Główna pętla gry
def main():
    clock = pygame.time.Clock()
    current_scene = "menu"
    menu = MenuScene(images)
    game = None

    while True:
        clock.tick(60)
        events = pygame.event.get()

        if current_scene == "menu":
            result = menu.handle_events(events)
            if result:
                
                if result == "stage_1":
                    cells = stages.get_stage_1(images)
                elif result == "stage_2":
                    cells = stages.get_stage_2(images)
                elif result == "stage_3":
                    cells = stages.get_stage_3(images)
                else:
                    cells = []

                game = GameScene(cells, images)
                current_scene = "game"
            menu.draw(WINDOW)

        elif current_scene == "game":
            result = game.handle_events(events)
            if result:
                menu = MenuScene(images)
                current_scene = "menu"
            else:
                game.update()
                game.draw(WINDOW)

        pygame.display.flip()


if __name__ == "__main__":
    main()
