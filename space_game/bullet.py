import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2

from config import screen_width, screen_heigth, ImageNames, heroes, enemies
from tools import Image


class Bullet(Sprite):
    def __init__(self, x, y, group, speed: V2, damage=10,
                 image=ImageNames.bullet3x7, angle=90, size=2):
        super().__init__()
        self.image = Image(image).rot_center(angle).scale(size).surf
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage
        self.add(group)

    def update(self):
        if 0 < self.rect.centerx < screen_width:
            self.rect.centerx += self.speed.x
        else:
            self.kill()

        if 0 < self.rect.centery < screen_heigth:
            self.rect.centery += self.speed.y
        else:
            self.kill()
