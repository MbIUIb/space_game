from enum import Enum

import pygame as pg

from config import MenuState, PauseState, MENU_NONACTIVE, MENU_ACTIVE


class SettingsState(Enum):
    pass


class Base:
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        pg.mouse.set_visible(True)

        self._screen: pg.Surface = screen
        self._padding = padding
        self._font = pg.font.Font(fontname, fontsize)
        if not self._states:
            self._states = tuple()
        self._texts = self._init_renders()
        self._block_rect = self._init_block_rect()
        self._texts_rects = self._init_text_rects()
        self._current = 0

        self.game_state = game_state
    
    def _init_renders(self) -> tuple:
        return tuple(self._font.render(state.value, False, 0xFF0000FF)
                     for state in self._states)
    
    def _init_block_rect(self) -> pg.Rect:
        rect = pg.Rect(0, 0, 0, 0)
        rect.w = max((text.get_rect().w for text in self._texts))
        rect.h = max((text.get_rect().h for text in self._texts)) + self._padding
        rect.h = rect.h * len(self._texts) - self._padding
        rect.centerx, rect.centery = self._screen.get_rect().center
        return rect

    def _init_text_rects(self) -> tuple:
        rects = []
        y = self._block_rect.y
        for text in self._texts:
            rect = text.get_rect()
            rect.centerx = self._block_rect.centerx
            rect.y = y
            rects.append(rect)
            y += rect.h + self._padding
        return tuple(rects)

class Menu(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        self._states = tuple(MenuState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

    def update(self, keys):
        change_state = False
        self.game_state = self.game_state.menu

        for event in pg.event.get():
            clicked = False

            if event.type == pg.QUIT:
                self.game_state = self.game_state.exit
            elif event.type == pg.MOUSEBUTTONDOWN:
                clicked = True

            for idx, rect in enumerate(self._texts_rects):
                if rect.collidepoint(pg.mouse.get_pos()):
                    self._current = idx

                    if clicked:
                        change_state = True

        if keys[pg.K_RETURN] or keys[pg.K_SPACE]:
            change_state = True

        if change_state:
            match self._states[self._current]:
                case MenuState.play:
                    self.game_state = self.game_state.play
                case MenuState.records:
                    pass
                case MenuState.settings:
                    pass
                case MenuState.exit:
                    self.game_state = self.game_state.exit

    def draw(self):
        self._screen.fill((0, 0, 0))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE
            text = self._font.render(self._states[idx].value, False, color)
            self._screen.blit(text, rect)


class Pause(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        self._states = tuple(PauseState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

    def update(self, keys):
        change_state = False
        self.game_state = self.game_state.pause

        for event in pg.event.get():
            clicked = False

            if event.type == pg.QUIT:
                self.game_state = self.game_state.exit
            elif event.type == pg.MOUSEBUTTONDOWN:
                clicked = True

            for idx, rect in enumerate(self._texts_rects):
                if rect.collidepoint(pg.mouse.get_pos()):
                    self._current = idx

                    if clicked:
                        change_state = True

        if keys[pg.K_RETURN] or keys[pg.K_SPACE]:
            change_state = True

        if change_state:
            match self._states[self._current]:
                case PauseState.resume:
                    self.game_state = self.game_state.play
                case PauseState.restart:
                    pass
                case PauseState.exit:
                    self.game_state = self.game_state.menu

    def draw(self):
        self._screen.fill((0, 0, 0))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE
            text = self._font.render(self._states[idx].value, False, color)
            self._screen.blit(text, rect)
