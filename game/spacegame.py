import pygame

from config import *
from starship import Starship
from background_stars import create_stars


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

mouse_control = True
mouse_visible = True
pygame.mouse.set_visible(mouse_visible)

game = True


while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        elif event.type == pygame.USEREVENT:
            create_stars(stars)

    if mouse_control:
        mouse_pos = pygame.mouse.get_pos()
        hero.follow_mouse(mouse_pos)
    else:
        # it is necessary to process 'if'-s in separate constructions
        keys = pygame.key.get_pressed()
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

    # third drawing
    screen.blit(hero.image, hero.rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
