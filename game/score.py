import pygame as pg

from config import SCORE, FontNames, screen


class Score:
    def __init__(self, fontname: str, fontsize: int = 30):
        self.score = 0
        self.font = pg.font.Font(fontname, fontsize)
        self._score_surf: pg.Surface = None
        self._score_rect: pg.Rect = None

    def __add__(self, score):
        self.score += score

    def update(self):
        self._score_surf = self.font.render(f'score: {self.score}', 1, SCORE)
        self._score_rect = self._score_surf.get_rect(topleft=(0, 0))

    def draw(self):
        screen.blit(self._score_surf, self._score_rect)
