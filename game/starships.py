from time import time
import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2 as V2

from config import OUTLINE, HP, screen_width, screen_heigth, screen, hero_bullets, enemy_bullets
from tools import load_image, unscale_image, rot_center
from bullet import Bullet


class StarShip(Sprite):
    def __init__(self, x, y, image, angle, group):
        super().__init__()
        self.vel = V2()
        self.image = rot_center(load_image(image), angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 100
        self.speed = 7
        self.speed4mouse = 12

        # bullet specification
        self.bullets = pygame.sprite.Group()
        self.bullet_pos_x = 0
        self.bullet_pos_y = 35
        self.bullet_speed = V2(0, -15)
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
        if fire_time - self.fire_flag > self.fire_pace:
            self.fire_flag = fire_time
            return Bullet(self.rect.centerx + self.bullet_pos_x,
                          self.rect.centery + self.bullet_pos_y,
                          self.bullets,
                          self.bullet_speed,
                          self.bullet_damage)

    def destruction(self):
        if self.health <= 0:
            self.detonation()
        else:
            # destruction animation
            pass

    def detonation(self):
        self.kill()
        # detonation animation

    def collide_bullets(self, group):
        for bullet in group:
            if pygame.sprite.collide_mask(self, bullet):
                if self.health > 0:
                    self.health -= bullet.damage
                    self.destruction()
                bullet.kill()

    def __del__(self):
        print("starship del")


class HeroStarShip(StarShip):
    def __init__(self, x, y, image, angle, group):
        super().__init__(x, y, image, angle, group)

        self.bullets = hero_bullets
        self.bullet_pos_y = -35
        # self.bullet_speed.scale_to_length(15)
        self.bullet_damage = 10

        self.hpbar = Health(self.health, 250, 15)

    def update(self):
        self.collide_bullets(enemy_bullets)
        self.hpbar.update(660, self.hpbar.bar_height, self.health)


x_direction = 1
class EnemyStarShip(StarShip):
    def __init__(self, x, y, image, angle, group):
        super().__init__(x, y, image, angle, group)
        self.speed = 3

        self.bullets = enemy_bullets
        self.bullet_speed = V2(0, 7)
        self.fire_pace = 1

        self.hpbar = Health(self.health)

    def update(self):
        global x_direction
        if self.rect.centerx < 50:
            x_direction = 1
        if self.rect.centerx > 750:
            x_direction = -1
        self.rect.centerx += self.speed * x_direction

        self.shoot()
        self.collide_bullets(hero_bullets)

        self.hpbar.update(self.rect.centerx, self.rect.centery-45, self.health)


class Health:
    def __init__(self, full_health, bar_width=50, bar_heigth=5):
        self.bar_width = bar_width
        self.bar_height = bar_heigth
        self.full_health = full_health
        self.surface = pygame.Surface((bar_width, bar_heigth))

    def update(self, x, y, curr_health):
        if curr_health < 0:
            curr_health = 0

        fill = curr_health/100 * self.bar_width
        fill_rect = pygame.Rect(0, 0, fill, self.bar_height)

        self.surface.fill(OUTLINE)
        pygame.draw.rect(self.surface, HP, fill_rect)
        screen.blit(self.surface, (x-self.bar_width//2, y-self.bar_height//2))
