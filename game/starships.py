from time import time
import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2

from config import screen_width, screen_heigth
from tools import load_image, unscale_image
from bullet import Bullet


class StarShip(Sprite):
    def __init__(self, x, y, image, group):
        super().__init__()
        self.vel = V2()
        self.image = load_image(image)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.speed = 7
        self.speed4mouse = None

        # bullet specification
        self.bullet_speed = None
        self.bullet_damage = None
        self.fire_pace = 0.15
        self.fire_flag = 0

        self.add(group)

    def left_movement(self):
        self.rect.centerx -= self.speed
        if self.rect.centerx < 0:
            self.rect.centerx = 0

    def right_movement(self):
        self.rect.centerx += self.speed
        if self.rect.centerx > screen_width:
            self.rect.centerx = screen_width

    def up_movement(self):
        self.rect.centery -= self.speed
        if self.rect.centery < 0:
            self.rect.centery = 0

    def down_movement(self):
        self.rect.centery += self.speed
        if self.rect.centery > screen_heigth:
            self.rect.centery = screen_heigth

    def follow_mouse(self, mouse_pos):
        """experimental function"""
        self.vel.update(mouse_pos[0] - self.x, mouse_pos[1] - self.y)

        if self.vel.length():
            self.vel.scale_to_length(self.speed4mouse)

        if abs(self.rect.centerx - mouse_pos[0]) >= self.speed // 2:
            self.rect.centerx += self.vel.x
        if abs(self.rect.centery - mouse_pos[1]) >= self.speed // 2:
            self.rect.centery += self.vel.y

    def shoot(self, group):
        fire_time = time()
        if fire_time - self.fire_flag > self.fire_pace:
            self.fire_flag = fire_time
            return Bullet(self.rect.centerx, self.rect.centery-45, group, self.bullet_damage, self.bullet_speed)


class HeroStarShip(StarShip):
    def __init__(self, x, y, image, group):
        super().__init__(x, y, image, group)
        self.speed4mouse = 12

        self.bullet_speed = 15
        self.bullet_damage = 10


x_direction = 1
class EnemyStarShip(StarShip):
    def __init__(self, x, y, image, group):
        super().__init__(x, y, image, group)

        self.bullet_speed = 7
        self.bullet_damage = 5
        self.fire_pace = 0.5

    def update(self):
        global x_direction
        if self.rect.centerx < 50:
            x_direction = 1
        if self.rect.centerx > 750:
            x_direction = -1
        self.rect.centerx += self.speed * x_direction

    def shoot(self, group):
        fire_time = time()
        if fire_time - self.fire_flag > self.fire_pace:
            self.fire_flag = fire_time
            return Bullet(self.rect.centerx, self.rect.centery+45, group, self.bullet_damage, self.bullet_speed)
