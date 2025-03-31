# animated_bullet.py
import pygame
import math

class AnimatedBullet:
    def __init__(self, start_cell, end_cell, speed=2):  # speed w pikselach/klatkę
        self.start_cell = start_cell
        self.end_cell = end_cell
        self.speed = speed  # odległość w pikselach na klatkę

        dx = end_cell.x - start_cell.x
        dy = end_cell.y - start_cell.y
        self.distance = math.hypot(dx, dy)
        self.total_frames = self.distance / self.speed if self.distance != 0 else 1
        self.progress = 0.0
        self.done = False

    def update(self, mutual=False):
        if not self.done:
            self.progress += 1 / self.total_frames
            if self.progress >= 1.0:
                self.progress = 1.0
                self.done = True
            elif mutual and self.progress >= 0.5:
                self.progress = 0.5
                self.done = True

    def draw(self, surface):
        sx, sy = self.start_cell.x, self.start_cell.y
        ex, ey = self.end_cell.x, self.end_cell.y
        bx = sx + (ex - sx) * self.progress
        by = sy + (ey - sy) * self.progress
        pygame.draw.circle(surface, (255, 255, 255), (int(bx), int(by)), 6)

    # def collides_with(self, other):
    #     if self.source == other.target and self.target == other.source:
    #         distance = self.position.distance_to(other.position)
    #         return distance < self.radius * 2  # lub np. 10 pikseli
    #     return False

