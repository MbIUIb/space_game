import pygame
# colors
SPACE = (3, 4, 49)
OUTLINE = (250, 65, 65)
HP = (0, 255, 108)
SCORE = (206, 137, 255)
# STAR_lvl1 = (253, 249, 255)
# STAR_lvl2 = (198, 198, 206)
# STAR_lvl3 = (109, 102, 114)

# fonts
arkhip = 'assets/fonts/Arkhip.ttf'
impact = 'assets/fonts/Impact.ttf'
wiguru = 'assets/fonts/WiGuru.ttf'

# screen
icon = 'icon.png'
game_name = 'Space Game'
screen_width = 800
screen_heigth = 800
screen = pygame.display.set_mode((screen_width, screen_heigth))

# initial mouse control settings
mouse_control = False
mouse_visible = False

# sprite groups
stars = pygame.sprite.Group()
heroes = pygame.sprite.Group()
hero_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

FPS = 60

star_config = {'star_lvl1': 4,
               'star_lvl2': 3,
               'star_lvl3': 2}
