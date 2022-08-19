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
    icon = 'assets/images/icon.png'
    enemy = 'assets/images/enemy.png'
    bullet3x10 = 'assets/images/bullet3x10.png'


class GameState(Enum):
    menu = 'menu'
    play = 'play'
    pause = 'pause'
    exit = 'exit'


class MenuState(Enum):
    play = 'new game'
    records = 'records'
    settings = 'settings'
    exit = 'exit'


class PauseState(Enum):
    resume = 'resume'
    restart = 'restart'
    exit = 'exit'


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
