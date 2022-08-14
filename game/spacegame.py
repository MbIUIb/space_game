import pygame

from config import *
from starships import HeroStarShip, EnemyStarShip
from background_stars import create_stars
from tools import load_image

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_heidth))

icon = load_image(icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(game_name)

clock = pygame.time.Clock()

# user events
FLYING_STAR = pygame.event.custom_type()
pygame.time.set_timer(FLYING_STAR, 70)
SHOOTING_HERO = pygame.event.custom_type()
pygame.time.set_timer(SHOOTING_HERO, 150)

# sprite groups
stars = pygame.sprite.Group()
hero_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

hero = HeroStarShip(screen_width // 2, screen_heidth - 100)
enemy = EnemyStarShip(screen_width // 2, 100)

pygame.mouse.set_visible(mouse_visible)

running_game = True

while running_game:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False
        elif event.type == FLYING_STAR:
            create_stars(stars)
        elif event.type == SHOOTING_HERO:
            if keys[pygame.K_SPACE]:
                hero.shoot(hero_bullets)

    if mouse_control:
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

    # firstly drawing
    screen.fill(SPACE)

    # secondly drawing
    stars.draw(screen)
    stars.update(screen_heidth)

    hero_bullets.draw(screen)
    hero_bullets.update(-1)

    # third drawing
    screen.blit(hero.image, hero.rect)
    screen.blit(enemy.image, enemy.rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
