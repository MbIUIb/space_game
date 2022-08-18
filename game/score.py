import pygame
from config import SCORE, arkhip, screen
pygame.init()


class Score:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(arkhip, 30)

    def addition(self, score):
        self.score += score

    def update(self):
        score_txt = self.font.render(f'score: {self.score}', 1, SCORE)
        pos = score_txt.get_rect(topleft=(0, 0))
        screen.blit(score_txt, pos)
