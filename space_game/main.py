from config import *
from starships import HeroStarShip, create_enemy, ship_groups_collision
from background_stars import create_stars
from tools import Image
from score import Score
from menu import BeginMenu, Registration, Login, Menu, Pause


pg.init()

screen = pg.display.set_mode((screen_width, screen_heigth))

icon = Image(ImageNames.hero_ship1).surf
pg.display.set_icon(icon)
pg.display.set_caption(game_name)

clock = pg.time.Clock()

# user events
FLYING_STAR = pg.event.custom_type()
pg.time.set_timer(FLYING_STAR, 70)

score = Score(FontNames.broken_console)
hero = HeroStarShip(screen_width // 2, screen_heigth - 100, ImageNames.hero_ship1, 90,
                    heroes, score, max_health=200)
game_objs = stars, hero_bullets, enemy_bullets, heroes, enemies, hero, score

pg.mouse.set_visible(mouse_visible)

running_game = True

state = GameState.begin_menu
begin_menu = BeginMenu(FontNames.broken_console, state, screen)
registration = Registration(FontNames.broken_console, state, screen)
login = Login(FontNames.broken_console, state, screen)
menu = Menu(FontNames.broken_console, state, screen)
pause = Pause(FontNames.broken_console, state, screen, hero)

while running_game:
    keys = pg.key.get_pressed()
    events = pg.event.get()

    for event in events:
        if event.type == pg.QUIT:
            running_game = False

    match state:

        case state.begin_menu:
            begin_menu.update(events)
            state = begin_menu.game_state
            begin_menu.draw()

        case state.registration:
            registration.update(events)
            state = registration.game_state
            registration.draw()

        case state.login:
            login.update(events)
            state = login.game_state
            login.draw()

        case state.menu:
            menu.update(events)
            state = menu.game_state
            menu.draw()

        case state.records:
            pass

        case state.play:
            if keys[pg.K_ESCAPE]:
                state = state.pause
                pause.screen = screen

            for event in events:
                if event.type == FLYING_STAR:
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
            if keys[pg.K_q]:
                hero.score.score = 4900

            if len(enemies) < 4:
                if 0 <= score.score < 1000:
                    create_enemy(score, 50)
                elif 1000 <= score.score < 2000:
                    create_enemy(score, 200, 150)
                    hero.bullet_damage = 15
                elif 2000 <= score.score < 2700:
                    create_enemy(score, 500, 230)
                    hero.bullet_damage = 30
                elif 2700 <= score.score < 5000:
                    create_enemy(score, 1000, 415)
                    hero.bullet_damage = 40
                elif 5000 <= score.score:
                    create_enemy(score, 10000, 740)
                    hero.bullet_damage = 75
                    hero.image = Image(ImageNames.hero_ship2).rot_center(90).surf
                    hero.lvl = 2

            if hero.health <= 0 and not len(hero_bullets):
                state = state.pause

            for enemy in enemies:
                if enemy.rect.centery >= screen_heigth-50:
                    hero.health = 0

            screen.fill(SPACE)

            stars.update(screen_heigth)
            hero_bullets.update()
            enemy_bullets.update()
            heroes.update()
            enemies.update()
            score.update()
            ship_groups_collision(heroes, enemies)

            stars.draw(screen)
            hero_bullets.draw(screen)
            enemy_bullets.draw(screen)
            enemies.draw(screen)
            heroes.draw(screen)
            hero.draw()
            score.draw()

        case state.pause:
            pause.update(events)
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
