# animated_connection.py
import pygame
import colors
from animated_bullet import AnimatedBullet


class AnimatedConnection:
    def __init__(self, start_cell, end_cell, speed=0.01):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.progress = 0.0
        self.speed = speed
        self.done = False
        self.bullets = []
        self.bullets_to_fire = 0
        self.mark_for_removal = False  # zainicjowane przez AI
        self.removal_progress = 0.0
        self.to_destroy = False

    def update(self, shoot):
        mutual = (self.end_cell in self.start_cell.connections and 
        self.start_cell in self.end_cell.connections)
        if not self.done:
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 1.0
                self.done = True
                self.start_cell.connections.append(self.end_cell)
        else:
            # AI-controlled strzały
            if self.bullets_to_fire > 0:
                self.bullets_to_fire -= 1
                bullet = AnimatedBullet(self.start_cell, self.end_cell)
                self.bullets.append(bullet)

            # shoot z timera
            if shoot and self.start_cell.units > 0:
                self.start_cell.units -= 1
                bullet = AnimatedBullet(self.start_cell, self.end_cell)
                self.bullets.append(bullet)

            for bullet in self.bullets:
                bullet.update(mutual)
                if bullet.done and not mutual:
                    if self.start_cell.owner == self.end_cell.owner:
                        self.end_cell.units += 1
                        if self.start_cell.type == "defence":
                            self.end_cell.units += 1
                    else:
                        self.end_cell.units -= 1
                        if self.start_cell.type == "attack":
                            self.end_cell.units -= 1
                        if self.end_cell.units < 0:
                            self.end_cell.owner = self.start_cell.owner
                            self.end_cell.units = abs(self.end_cell.units)

        # Usuń zakończone kule
        self.bullets = [b for b in self.bullets if not b.done]

        # Animacja zanikania
        if self.mark_for_removal and self.done:
            self.removal_progress += 0.05
            if self.removal_progress >= 1.0:
                self.to_destroy = True

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        sx = self.start_cell.x + ox
        sy = self.start_cell.y + oy
        ex = self.end_cell.x + ox
        ey = self.end_cell.y + oy
        mid_x = (sx + ex) / 2
        mid_y = (sy + ey) / 2

        alpha = int(255 * (1 - self.removal_progress))
        color1 = (colors.GREEN + (alpha,)) if self.start_cell.owner == "player" else (colors.RED + (alpha,))
        color2 = (colors.GREEN + (alpha,)) if self.end_cell.owner == "player" else (colors.RED + (alpha,))

        if self.removal_progress > 0:
            temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            target_surface = temp_surface
        else:
            target_surface = surface
            color1 = colors.GREEN if self.start_cell.owner == "player" else colors.RED
            color2 = colors.GREEN if self.end_cell.owner == "player" else colors.RED


        mutual = (self.end_cell in self.start_cell.connections and 
                self.start_cell in self.end_cell.connections)
        if mutual:
            if self.progress <= 0.5:
                t = self.progress / 0.5
                current_mid_x = sx + (mid_x - sx) * t
                current_mid_y = sy + (mid_y - sy) * t
                pygame.draw.line(target_surface, color1, (sx, sy), (current_mid_x, current_mid_y), 5)
            else:
                pygame.draw.line(target_surface, color1, (sx, sy), (mid_x, mid_y), 5)
                t = (self.progress - 0.5) / 0.5
                current_end_x = mid_x + (ex - mid_x) * t
                current_end_y = mid_y + (ey - mid_y) * t
                pygame.draw.line(target_surface, color2, (mid_x, mid_y), (current_end_x, current_end_y), 5)
        else:
            current_x = sx + (ex - sx) * self.progress
            current_y = sy + (ey - sy) * self.progress
            pygame.draw.line(target_surface, color1, (sx, sy), (current_x, current_y), 5)

        if self.removal_progress > 0:
            surface.blit(temp_surface, (0, 0))

        for bullet in self.bullets:
            bullet.draw(surface, offset)

