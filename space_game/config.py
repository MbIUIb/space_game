from dataclasses import dataclass
from enum import Enum

import pygame as pg


@dataclass
class FontNames:
    broken_console = 'assets/fonts/Broken Console Regular.ttf'
    arkhip = 'assets/fonts/Arkhip.ttf'
    impact = 'assets/fonts/Impact.ttf'
    wiguru = 'assets/fonts/WiGuru.ttf'


@dataclass
class ImageNames:
    hero_ship1 = 'assets/images/hero_lvl1.png'
    hero_ship2 = 'assets/images/hero_lvl2.png'
    enemy = 'assets/images/enemy.png'
    bullet3x7 = 'assets/images/bullet3x7.png'
    bullet3x10 = 'assets/images/bullet3x10.png'


class GameState(Enum):
    begin_menu = 'begin_menu'
    registration = 'registration'
    login = 'login'
    menu = 'menu'
    records = 'records'
    play = 'play'
    pause = 'pause'
    restart = 'restart'
    exit = 'exit'


class BeginMenuState(Enum):
    login = 'login'
    register = 'register'
    exit = 'exit'


class RegistrState(Enum):
    user_login = '__login__'
    user_password = '__password__'
    register = 'register'
    back = 'back'


class LoginState(Enum):
    user_login = '__login__'
    user_password = '__password__'
    login = 'login'
    back = 'back'


class MenuState(Enum):
    play = 'new game'
    records = 'records'
    settings = 'settings'
    logout = 'log out'
    exit = 'exit'


class PauseState(Enum):
    resume = 'resume'
    restart = 'restart'
    exit = 'exit to menu'


class DBAutentication(Enum):
    login_error = 'login error'
    pass_error = 'password error'
    successful = 'successful'


# COLORS

SPACE = (3, 4, 49)
OUTLINE = (250, 65, 65)
HP = (0, 255, 108)
SCORE = (206, 137, 255)
MENU_NONACTIVE = (55, 33, 52)
MENU_ACTIVE = (71, 68, 118)
# STAR_lvl1 = (253, 249, 255)
# STAR_lvl2 = (198, 198, 206)
# STAR_lvl3 = (109, 102, 114)


# SCREEN

icon = 'assets/images/icon.png'
game_name = 'Space Game'
screen_width = 800
screen_heigth = 800
screen = pg.display.set_mode((screen_width, screen_heigth))
FPS = 60


# INITIAL MOUSE CONTROL SETTINGS

mouse_control = False
mouse_visible = False


# SPRITE GROUPS

class EnemiesGroup(pg.sprite.Group):
    def draw(self, surf):
        pg.sprite.Group.draw(self, surf)
        for sprite in self.sprites():
            sprite.hpbar.draw()

stars = pg.sprite.Group()
heroes = pg.sprite.Group()
hero_bullets = pg.sprite.Group()
enemies = EnemiesGroup()
enemy_bullets = pg.sprite.Group()

                
star_config = {'assets/images/star_lvl1': 4,
               'assets/images/star_lvl2': 3,
               'assets/images/star_lvl3': 2}

database = 'assets/database/database.db'
