import pygame
import colors

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
        if not self.done:
            self.progress += self.speed
            if self.progress >= 1.0:
                self.progress = 1.0
                self.done = True
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
                bullet.update()
                if bullet.done:
                    if self.start_cell.owner == self.end_cell.owner:
                        self.end_cell.units += 1
                    else:
                        self.end_cell.units -= 1
                        if self.end_cell.units < 0:
                            self.end_cell.owner = self.start_cell.owner
                            self.end_cell.units = abs(self.end_cell.units)

        # Usuń zakończone kule
        self.bullets = [b for b in self.bullets if not b.done]

        # Animacja zanikania
        if self.mark_for_removal and self.done and not self.bullets:
            self.removal_progress += 0.05
            if self.removal_progress >= 1.0:
                self.to_destroy = True

    def draw(self, surface):
        sx, sy = self.start_cell.x, self.start_cell.y
        ex, ey = self.end_cell.x, self.end_cell.y
        mx = sx + (ex - sx) * self.progress
        my = sy + (ey - sy) * self.progress

        # Oblicz kolor z przezroczystością (zanikanie)
        if self.removal_progress > 0:
            alpha = int(255 * (1 - self.removal_progress))
            color = (0, 0, 255, alpha)
            temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.line(temp_surface, color, (sx, sy), (mx, my), 5)
            surface.blit(temp_surface, (0, 0))
        else:
            pygame.draw.line(surface, colors.BLUE, (sx, sy), (mx, my), 5)

        for bullet in self.bullets:
            bullet.draw(surface)


class AnimatedBullet:
    def __init__(self, start_cell, end_cell, speed=0.005):
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.progress = 0.0
        self.speed = speed
        self.done = False

    def update(self):
        self.progress += self.speed
        if self.progress >= 1.0:
            self.progress = 1.0
            self.done = True

    def draw(self, surface):
        sx, sy = self.start_cell.x, self.start_cell.y
        ex, ey = self.end_cell.x, self.end_cell.y
        bx = sx + (ex - sx) * self.progress
        by = sy + (ey - sy) * self.progress
        pygame.draw.circle(surface, (255, 255, 255), (int(bx), int(by)), 6)
