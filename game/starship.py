from config import screen_width, screen_heidth
from pygame.sprite import Sprite
import pygame


class Starship(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        image = pygame.image.load('res/icon.png')
        self.image = pygame.transform.scale(image, (image.get_width() // 4, image.get_height() // 4)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 100
        self.speed = 7

    def coordinates_update(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def left_movement(self):
        self.x -= self.speed
        self.coordinates_update()

        if self.x < 0:
            self.x = 0+5

    def right_movement(self):
        self.x += self.speed
        self.coordinates_update()

        if self.x > screen_width:
            self.x = screen_width-5

    def up_movement(self):
        self.y -= self.speed
        self.coordinates_update()

        if self.y < 0:
            self.y = 0+5

    def down_movement(self):
        self.y += self.speed
        self.coordinates_update()

        if self.y > screen_heidth:
            self.y = screen_heidth-5

    def follow_mouse(self, mouse_pos):
        if self.x < mouse_pos[0]:
            self.x += self.speed
        elif self.x > mouse_pos[0]:
            self.x -= self.speed

        if self.y < mouse_pos[1]:
            self.y += self.speed
        elif self.y > mouse_pos[1]:
            self.y -= self.speed

        self.coordinates_update()
