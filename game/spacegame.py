from config import *
from starship import Starship
from background_stars import create_stars
import pygame
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_heidth))

icon = pygame.image.load('res/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Space Game')

clock = pygame.time.Clock()
# time between creation of stars
pygame.time.set_timer(pygame.USEREVENT, 70)

stars = pygame.sprite.Group()
hero = Starship(screen_width//2, screen_heidth//2)

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.USEREVENT:
            create_stars(stars)

    # it is necessary to process if-s in separate constructions
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        hero.left_movement()
    if keys[pygame.K_RIGHT]:
        hero.right_movement()
    if keys[pygame.K_UP]:
        hero.up_movement()
    if keys[pygame.K_DOWN]:
        hero.down_movement()

    screen.fill(SPACE)


    stars.draw(screen)
    stars.update(screen_heidth)


    screen.blit(hero.image, hero.rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
