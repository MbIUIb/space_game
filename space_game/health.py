import pygame as pg

from config import screen, OUTLINE, HP


class Health:
    def __init__(self, full_health: int, w: int = 50, h: int = 5):
        self._bar_rect = pg.Rect(0, 0, w, h)
        self._full_health = full_health
        self._curr_health = full_health
        self._surf = pg.Surface(self._bar_rect.bottomright)

        self._x: int = 0
        self._y: int = 0

    @property
    def h(self):
        return self._bar_rect.h

    def update(self, x, y, curr_health):
        self._curr_health = curr_health if curr_health > 0 else 0

        self._x = x
        self._y = y

    def draw(self):
        fill_rect = self._bar_rect.copy()
        fill_rect.w = fill_rect.w * self._curr_health / self._full_health

        self._surf.fill(OUTLINE)
        pg.draw.rect(self._surf, HP, fill_rect)
        screen.blit(self._surf, (self._x-self._bar_rect.centerx, self._y-self._bar_rect.centery))
