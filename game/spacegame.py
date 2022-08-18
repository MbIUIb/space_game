from enum import Enum

import pygame

from config import *
from starships import HeroStarShip, EnemyStarShip, create_enemy
from background_stars import create_stars
from tools import load_image
from menu import Menu


class State(Enum):
    menu = 'menu'
    play = 'play'
    exit = 'exit'
    

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

pygame.mouse.set_visible(mouse_visible)

running_game = True
state = State.menu
menu = Menu(FontNames.broken_console, state, screen)

while running_game:
    keys = pygame.key.get_pressed()

    match state:
        case state.menu:
            menu.update(keys)
            state = menu.game_state

            menu.draw()

        case state.play:
            if keys[pygame.K_ESCAPE]:
                state = state.menu

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
                if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[1092]:
                    hero.left_movement()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[1074]:
                    hero.right_movement()
                if keys[pygame.K_UP] or keys[pygame.K_w] or keys[1094]:
                    hero.up_movement()
                if keys[pygame.K_DOWN] or keys[pygame.K_s] or keys[1099]:
                    hero.down_movement()
                if keys[pygame.K_SPACE]:
                    hero.shoot()

            if len(enemies) < 3:
                create_enemy()

            screen.fill(SPACE) # before starships draw
            stars.update(screen_heigth)
            hero_bullets.update()
            enemy_bullets.update()
            heroes.update()
            enemies.update()

            stars.draw(screen)
            hero_bullets.draw(screen)
            enemy_bullets.draw(screen)
            enemies.draw(screen)
            heroes.draw(screen)

        case state.exit:
            running_game = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
