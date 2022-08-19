import pygame as pg
from pygame import transform


class Image:
    def __init__(self, filename: str = '', surf: pg.Surface = None):
        self._surf = None
        self._filename = None

        if surf:
            self._surf = surf
        elif filename:
            self._filename = filename
            self.load()

    @property
    def surf(self):
        if not self._surf:
            raise Exception('surf is not init')
        return self._surf

    def load(self, alpha: bool = True):
        image = pg.image.load(self._filename)
        self._surf = image.convert_alpha() if alpha else image.convert()
        return Image(surf=self._surf)

    def scale(self, value: float):
        w = self._surf.get_width()
        h = self._surf.get_height()
        self._surf = transform.scale(self._surf, (w * value, h * value))
        return Image(surf=self._surf)

    def rot_center(self, angle: int):
        self._surf = pg.transform.rotate(self._surf, angle)
        return Image(surf=self._surf)

