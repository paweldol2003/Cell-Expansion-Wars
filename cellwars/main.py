import pygame
import sys
import stages
import cell
import scenes 
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cell Expansion Wars")

# Kolory
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
RED = (220, 20, 60)




# Główna pętla gry
def main():
    clock = pygame.time.Clock()
    current_scene = "menu"
    menu = scenes.MenuScene()
    game = None

    while True:
        clock.tick(60)
        events = pygame.event.get()

        if current_scene == "menu":
            result = menu.handle_events(events)
            if result:
                game = scenes.GameScene(result())

                current_scene = "game"
            menu.draw(WINDOW)

        elif current_scene == "game":
            result = game.handle_events(events)
            if result:
                menu = scenes.MenuScene()
                current_scene = "menu"
            else:
                game.update()
                game.draw(WINDOW)


        pygame.display.flip()


if __name__ == "__main__":
    main()
