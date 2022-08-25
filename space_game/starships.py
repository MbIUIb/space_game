from time import time
from random import randint

import pygame as pg

from config import (screen_width, screen_heigth, ImageNames, hero_bullets,
                   enemy_bullets, enemies, OUTLINE)
from tools import Image
from bullet import Bullet
from health import Health
from score import Score
from particles import ParticleSystem


class StarShip(pg.sprite.Sprite):
    def __init__(self, x, y, image, angle, group, score: Score, bullet_img=ImageNames.bullet3x7):
        super().__init__()
        # init states
        self.begin_x = x
        self.begin_y = y
        self.max_health = 100

        # ship spec
        self.vel = pg.Vector2()
        self.image = Image(image).rot_center(angle).surf
        self.rect = self.image.get_rect(center=(x, y))
        self.health = self.max_health
        self.speed = 7
        self.speed4mouse = 12
        self.score = score
        self.score_points = 0
        self.particles = ParticleSystem()

        # bullet spec
        self.bullet_img = bullet_img
        self.bullets = pg.sprite.Group()
        self.bullet_pos_x = 0
        self.bullet_pos_y = 35
        self.bullet_speed = pg.Vector2(0, -15)
        self.bullet_damage = 5
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
        self.vel.update(mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery)

        if self.vel.length():
            self.vel.scale_to_length(self.speed4mouse)

        if abs(self.rect.centerx - mouse_pos[0]) >= self.speed // 2:
            self.rect.centerx += self.vel.x
        if abs(self.rect.centery - mouse_pos[1]) >= self.speed // 2:
            self.rect.centery += self.vel.y

    def shoot(self):
        fire_time = time()
        if fire_time - self.fire_flag > self.fire_pace and self.health > 0:
            self.fire_flag = fire_time
            return Bullet(self.rect.centerx + self.bullet_pos_x,
                          self.rect.centery + self.bullet_pos_y,
                          self.bullets,
                          self.bullet_speed,
                          self.bullet_damage,
                          self.bullet_img)

    def update(self):
        self.destruction()

    def destruction(self):
        if self.health <= 0:
            self.score.score += self.score_points
            self.detonation()
        else:
            # destruction animation
            pass

    def detonation(self):
        self.kill()
        # detonation animation

    def collide_bullets(self, group):
        for bullet in group:
            if pg.sprite.collide_mask(self, bullet):
                if self.health > 0:
                    self.health -= bullet.damage
                bullet.kill()


class HeroStarShip(StarShip):
    def __init__(self, x, y, image, angle, group, score: Score):
        super().__init__(x, y, image, angle, group, score)
        self.particles = ParticleSystem(max_speed_x=2, max_speed_y=5)

        self.bullet_img = ImageNames.bullet3x10
        self.bullets = hero_bullets
        self.bullet_pos_y = -35
        # self.bullet_speed.scale_to_length(15)
        self.bullet_damage = 10

        self.hpbar = Health(self.health, 250, 15)
        self.group = group

    def update(self):
        super().update()
        self.particles.add_particles(self.rect.centerx, self.rect.bottom - 15)
        self.particles.update()

        self.collide_bullets(enemy_bullets)
        self.hpbar.update(660, self.hpbar.h, self.health)

    def draw(self):
        self.hpbar.draw()

    def restart(self):
        self.add(self.group)
        self.rect = self.image.get_rect(center=(self.begin_x, self.begin_y))
        self.health = self.max_health
        self.score.score = 0


class EnemyStarShip(StarShip):
    def __init__(self, x, y, image, angle, group, score: Score):
        super().__init__(x, y, image, angle, group, score)
        self.speed = 3
        self.score_points = 100
        self.particles = ParticleSystem(max_speed_x=1, max_speed_y=5, direction_y=-1, color=OUTLINE)

        self.bullets = enemy_bullets
        self.bullet_speed = pg.Vector2(0, 7)
        self.fire_pace = 1

        self.hpbar = Health(self.health)

        self.x_direction = 1
        self.y_direction = 1

    def update(self):
        super().update()
        self.particles.add_particles(self.rect.centerx, self.rect.top+20)
        self.particles.update()

        self.enemy_movement()

        self.shoot()
        self.collide_bullets(hero_bullets)

        self.hpbar.update(self.rect.centerx, self.rect.centery-45, self.health)

    def enemy_movement(self, type=1):
        match type:
            case 0: # static pos
                return
            case 1: # simple left-right movement
                if self.rect.centerx < 50:
                    self.x_direction = 1
                if self.rect.centerx > 750:
                    self.x_direction = -1
                self.rect.centerx += self.speed * self.x_direction
            case 2:
                # new type
                pass


def create_enemy(score: Score):
    x = randint(30, 770)
    y = randint(30, screen_heigth//2)

    return EnemyStarShip(x, y, ImageNames.enemy, -90, enemies, score)


def ship_groups_collision(hero_group, enemy_group):
    for hero in hero_group:
        for enemy in enemy_group:
            if not pg.sprite.collide_mask(hero, enemy):
                continue
            hero.health -= 0.5
            enemy.health -= 1
