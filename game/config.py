import pygame as pg


# colors
SPACE = (3, 4, 49)
# STAR_lvl1 = (253, 249, 255)
# STAR_lvl2 = (198, 198, 206)
# STAR_lvl3 = (109, 102, 114)

# screen
icon = 'icon.png'
game_name = 'Space Game'
screen_width = 800
screen_heigth = 800

# initial mouse control settings
mouse_control = False
mouse_visible = False

# sprite groups
stars = pg.sprite.Group()
heroes = pg.sprite.Group()
hero_bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
enemy_bullets = pg.sprite.Group()

FPS = 60

star_config = {'star_lvl1': 4,
               'star_lvl2': 3,
               'star_lvl3': 2}
