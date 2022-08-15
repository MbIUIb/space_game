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

hero = HeroStarShip(screen_width // 2, screen_heigth - 100, 'icon.png', heroes)
enemy = EnemyStarShip(screen_width // 2, 100, 'enemy.png', enemies)

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
            hero.shoot(hero_bullets)

    # firstly drawing
    screen.fill(SPACE)

    # secondly drawing
    stars.draw(screen)
    stars.update(screen_heigth)

    hero_bullets.draw(screen)
    hero_bullets.update(-1)

    enemy_bullets.draw(screen)
    enemy_bullets.update()

    # third drawing
    heroes.draw(screen)
    heroes.update()

    enemies.draw(screen)
    enemies.update()
    enemy.shoot(enemy_bullets)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
