import pygame as pg
from config import SCORE, FontNames, screen
pg.init()


class Score:
    def __init__(self):
        self.score = 0
        self.font = pg.font.Font(FontNames.arkhip, 30)

    def addition(self, score):
        self.score += score

    def update(self):
        score_txt = self.font.render(f'score: {self.score}', 1, SCORE)
        pos = score_txt.get_rect(topleft=(0, 0))
        screen.blit(score_txt, pos)
