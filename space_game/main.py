from enum import Enum

import pygame as pg

from config import *
from starships import HeroStarShip, create_enemy, ship_groups_collision
from background_stars import create_stars
from tools import Image
from score import Score
from menu import Menu, Pause


pg.init()

screen = pg.display.set_mode((screen_width, screen_heigth))

icon = Image(ImageNames.icon).surf
pg.display.set_icon(icon)
pg.display.set_caption(game_name)

clock = pg.time.Clock()

# user events
FLYING_STAR = pg.event.custom_type()
pg.time.set_timer(FLYING_STAR, 70)

score = Score(FontNames.broken_console)
hero = HeroStarShip(screen_width // 2, screen_heigth - 100, ImageNames.icon, 90,
                    heroes, score)
game_objs = stars, hero_bullets, enemy_bullets, heroes, enemies, hero, score

pg.mouse.set_visible(mouse_visible)

running_game = True
state = GameState.menu
menu = Menu(FontNames.broken_console, state, screen)
pause = Pause(FontNames.broken_console, state, screen, hero)

while running_game:
    keys = pg.key.get_pressed()

    match state:
        case state.menu:
            menu.update(keys)
            state = menu.game_state
            menu.draw()

        case state.play:
            if keys[pg.K_ESCAPE]:
                state = state.pause
                pause.screen = screen

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

            if hero.health <= 0 and not len(hero_bullets):
                state = state.pause

            stars.update(screen_heigth)
            hero_bullets.update()
            enemy_bullets.update()
            heroes.update()
            enemies.update()
            score.update()
            ship_groups_collision(heroes, enemies)

            screen.fill(SPACE)
            stars.draw(screen)
            hero_bullets.draw(screen)
            enemy_bullets.draw(screen)
            enemies.draw(screen)
            heroes.draw(screen)
            hero.draw()
            score.draw()

        case state.pause:
            pause.update(keys)
            state = pause.game_state
            pause.draw()

        case state.restart:
            hero.restart()
            enemies.empty()
            enemy_bullets.empty()
            state = state.play

        case state.exit:
            running_game = False

    pg.display.update()
    clock.tick(FPS)

pg.quit()
