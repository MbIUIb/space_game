import pygame
from pygame.sprite import Sprite
from random import randint
import random
from config import screen_width, star_config
from tools import load_image


class Star(Sprite):
    def __init__(self, x, speed, filename, group):
        Sprite.__init__(self)
        self.image = load_image(filename)
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.add(group)

    def update(self, *coords):
        if self.rect.y < coords[0]:
            self.rect.y += self.speed
        else:
            self.kill()


def create_stars(group):
    x = randint(0 , screen_width)
    sample = random.sample(star_config.items(), 1)

    return Star(x, sample[0][1], sample[0][0]+'.png', group)
