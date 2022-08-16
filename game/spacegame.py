import pygame

from config import *
from starships import HeroStarShip, EnemyStarShip
from background_stars import create_stars
from tools import load_image

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_heigth))

icon = load_image(icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(game_name)

clock = pygame.time.Clock()

# user events
FLYING_STAR = pygame.event.custom_type()
pygame.time.set_timer(FLYING_STAR, 70)

hero = HeroStarShip(screen_width // 2, screen_heigth - 100, 'icon.png', 90, heroes)
enemy = EnemyStarShip(screen_width // 2, 100, 'enemy.png', -90, enemies)

pygame.mouse.set_visible(mouse_visible)

running_game = True

while running_game:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        elif event.type == FLYING_STAR:
            create_stars(stars)

    if mouse_control and not keys[pygame.K_LALT]:
        mouse_pos = pygame.mouse.get_pos()
        hero.follow_mouse(mouse_pos)
    else:
        # it is necessary to process 'if'-s in separate constructions
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            hero.left_movement()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            hero.right_movement()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            hero.up_movement()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            hero.down_movement()
        if keys[pygame.K_SPACE]:
            hero.shoot()

    stars.update(screen_heigth)
    hero.bullets.update()
    enemy.bullets.update()
    heroes.update()
    enemies.update()
    enemy.shoot()

    screen.fill(SPACE)
    stars.draw(screen)
    hero.bullets.draw(screen)
    enemy.bullets.draw(screen)
    enemies.draw(screen)
    heroes.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
