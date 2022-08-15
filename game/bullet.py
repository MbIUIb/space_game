import pygame
from pygame.sprite import Sprite

from config import screen_width, screen_heigth
from tools import load_image


class Bullet(Sprite):
    def __init__(self, x, y, group, damage=10, speed=15):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.image = load_image('bullet3x10.png')
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.add(group)

    def update(self, updirection=1):
        if 0 < self.rect.centery < screen_heigth:
            self.rect.centery += self.speed * updirection
        else:
            self.kill()
