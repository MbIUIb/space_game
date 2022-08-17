import pygame

from config import screen, OUTLINE, HP


class Health:
    def __init__(self, full_health, bar_width=50, bar_heigth=5):
        self.bar_width = bar_width
        self.bar_height = bar_heigth
        self.full_health = full_health
        self.surface = pygame.Surface((bar_width, bar_heigth))

    def update(self, x, y, curr_health):
        if curr_health < 0:
            curr_health = 0

        fill = curr_health/100 * self.bar_width
        fill_rect = pygame.Rect(0, 0, fill, self.bar_height)

        self.surface.fill(OUTLINE)
        pygame.draw.rect(self.surface, HP, fill_rect)
        screen.blit(self.surface, (x-self.bar_width//2, y-self.bar_height//2))
