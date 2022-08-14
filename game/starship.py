import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2

from config import screen_width, screen_height


class Starship(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vel = V2()
        image = pygame.image.load('assets/icon.png')
        self.image = pygame.transform.scale(image, (image.get_width() // 4, image.get_height() // 4)).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 100
        self.speed = 12

    def coords_update(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def left_movement(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0+5
        self.coords_update()

    def right_movement(self):
        self.x += self.speed
        if self.x > screen_width:
            self.x = screen_width-5
        self.coords_update()

    def up_movement(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = 0+5
        self.coords_update()

    def down_movement(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = screen_height-5
        self.coords_update()

    def follow_mouse(self, mouse_pos):
        self.vel.update(mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        if self.vel.length():
            self.vel.scale_to_length(self.speed)

        if abs(self.x - mouse_pos[0]) >= self.speed // 2:
            self.x += self.vel.x
        if abs(self.y - mouse_pos[1]) >= self.speed // 2:
            self.y += self.vel.y

        self.coords_update()
