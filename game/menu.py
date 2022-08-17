from enum import Enum

import pygame as pg


class MeuState(Enum):
    pass


class SettingsState(Enum):
    pass


class Menu:
    def __init__(self, font: pg.font.Font, state, size: int = 72):
        self.font = font

    def update(self):
        pass

    def draw(self):
        pass
