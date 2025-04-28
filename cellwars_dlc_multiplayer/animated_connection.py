# animated_connection.py
import pygame
import colors
from animated_bullet import AnimatedBullet


class AnimatedConnection:
    def __init__(self, attacking_cell, attacked_cell, speed=0.005):
        self.attacking_cell = attacking_cell
        self.attacked_cell = attacked_cell
        self.progress = 0.0
        self.speed = speed
        self.done = False
        self.bullets = []
        self.mark_for_removal = False  
        self.removal_progress = 0.0
        self.to_destroy = False
        self.mutual = False  # czy połączenie jest wzajemne

    def update(self, scene, shoot):

        self.mutual = (self.attacked_cell in self.attacking_cell.connections and 
        self.attacking_cell in self.attacked_cell.connections)

        if not self.done:
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 1.0
                self.done = True
                self.attacking_cell.connections.append(self.attacked_cell)
        else:

            # shoot z timera
            if shoot and self.attacking_cell.units > 0:
                self.attacking_cell.units -= 1
                bullet = AnimatedBullet(self.attacking_cell, self.attacked_cell)
                self.bullets.append(bullet)

            for bullet in self.bullets:
                bullet.update(self.mutual)
                if bullet.done and not self.mutual:
                    if self.attacking_cell.owner == self.attacked_cell.owner and self.attacking_cell.owner_id == self.attacked_cell.owner_id:
                        self.attacked_cell.units += 1
                        if self.attacking_cell.type == "defence":
                            self.attacked_cell.units += 1
                    else:
                        self.attacked_cell.units -= 1
                        if self.attacking_cell.type == "attack":
                            self.attacked_cell.units -= 1
                            
                        if self.attacked_cell.units < 0: # zmiania właściciela
                            self.attacked_cell.owner = self.attacking_cell.owner
                            self.attacked_cell.owner_id = self.attacking_cell.owner_id
                            self.attacked_cell.units = abs(self.attacked_cell.units)
                            self.attacked_cell.color = self.attacking_cell.color
                            for anim in scene.animating_connections:
                                if anim.attacking_cell == self.attacked_cell:
                                    anim.mark_for_removal = True
        # Usuń zakończone kule
        self.bullets = [b for b in self.bullets if not b.done]

        # Animacja zanikania
        if self.mark_for_removal and self.done:
            self.removal_progress += 0.05
            if self.removal_progress >= 1.0:
                self.to_destroy = True
                if self.attacked_cell in self.attacking_cell.connections:
                    self.attacking_cell.connections.remove(self.attacked_cell)
                # jeśli było wzajemne, to usuń też attacked_cell → attacking_cell
                if self.attacking_cell in self.attacked_cell.connections:
                    self.attacked_cell.connections.remove(self.attacking_cell)

    def draw(self, surface, offset=(0, 0)):
        ox, oy = offset
        sx = self.attacking_cell.x + ox
        sy = self.attacking_cell.y + oy
        ex = self.attacked_cell.x + ox
        ey = self.attacked_cell.y + oy
        mid_x = (sx + ex) / 2
        mid_y = (sy + ey) / 2

        alpha = int(255 * (1 - self.removal_progress))

        color1 = self.attacking_cell.color + (alpha,)
        color2 = self.attacked_cell.color + (alpha,)

        if self.removal_progress > 0:
            temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            target_surface = temp_surface
        else:
            target_surface = surface
            color1 = self.attacking_cell.color
            color2 = self.attacked_cell.color

        if self.mutual:
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


