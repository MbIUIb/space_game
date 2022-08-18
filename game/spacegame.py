from enum import Enum

import pygame as pg

from config import *
from starships import HeroStarShip, EnemyStarShip, create_enemy
from background_stars import create_stars
from tools import load_image
from score import Score
from menu import Menu


class State(Enum):
    menu = 'menu'
    play = 'play'
    exit = 'exit'
    

pg.init()

screen = pg.display.set_mode((screen_width, screen_heigth))

icon = load_image(icon)
pg.display.set_icon(icon)
pg.display.set_caption(game_name)

clock = pg.time.Clock()

# user events
FLYING_STAR = pg.event.custom_type()
pg.time.set_timer(FLYING_STAR, 70)

score = Score(FontNames.arkhip)
hero = HeroStarShip(screen_width // 2, screen_heigth - 100, 'icon.png', 90,
                    heroes, score)

pg.mouse.set_visible(mouse_visible)

running_game = True
state = State.menu
menu = Menu(FontNames.broken_console, state, screen)

while running_game:
    keys = pg.key.get_pressed()

    match state:
        case state.menu:
            menu.update(keys)
            state = menu.game_state

            menu.draw()

        case state.play:
            if keys[pg.K_ESCAPE]:
                state = state.menu

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running_game = False
                elif event.type == FLYING_STAR:
                    create_stars(stars)

            if mouse_control and not keys[pg.K_LALT]:
                mouse_pos = pg.mouse.get_pos()
                hero.follow_mouse(mouse_pos)
            else:
                # it is necessary to process 'if'-s in separate constructions
                if keys[pg.K_LEFT] or keys[pg.K_a] or keys[1092]:
                    hero.left_movement()
                if keys[pg.K_RIGHT] or keys[pg.K_d] or keys[1074]:
                    hero.right_movement()
                if keys[pg.K_UP] or keys[pg.K_w] or keys[1094]:
                    hero.up_movement()
                if keys[pg.K_DOWN] or keys[pg.K_s] or keys[1099]:
                    hero.down_movement()
                if keys[pg.K_SPACE]:
                    hero.shoot()

            if len(enemies) < 3:
                create_enemy(score)

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
            score.draw()

        case state.exit:
            running_game = False

    pg.display.update()
    clock.tick(FPS)

pg.quit()
