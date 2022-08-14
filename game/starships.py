import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2

from config import screen_width, screen_heidth
from tools import load_image, unscale_image
from bullet import Bullet


class StarShip(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 7

    def coords_update(self):
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def left_movement(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
        self.coords_update()

    def right_movement(self):
        self.x += self.speed
        if self.x > screen_width:
            self.x = screen_width
        self.coords_update()

    def up_movement(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = 0
        self.coords_update()

    def down_movement(self):
        self.y += self.speed
        if self.y > screen_heidth:
            self.y = screen_heidth
        self.coords_update()


class HeroStarShip(StarShip):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vel = V2()
        self.image = load_image('icon.png')
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 100
        self.bullet_damage = 10
        self.bullet_speed = 15
        self.speed4mouse = 12

    def follow_mouse(self, mouse_pos):
        self.vel.update(mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        if self.vel.length():
            self.vel.scale_to_length(self.speed4mouse)

        if abs(self.x - mouse_pos[0]) >= self.speed // 2:
            self.x += self.vel.x
        if abs(self.y - mouse_pos[1]) >= self.speed // 2:
            self.y += self.vel.y

        self.coords_update()

    def shoot(self, group):
        return Bullet(self.x, self.y-45, group, self.bullet_damage, self.bullet_speed)


class EnemyStarShip(StarShip):
    def __init__(self, x, y, filename='enemy.png'):
        super().__init__(x, y)
        self.image = load_image(filename)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.health = 100
        self.bullet_damage = 5
        self.bullet_speed = 7
        self.speed = 5
