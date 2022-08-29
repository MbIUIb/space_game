from enum import Enum

import pygame as pg

from config import BeginMenuState, RegistrState, LoginState, MenuState, PauseState, DBAutentication, MENU_NONACTIVE, MENU_ACTIVE
from tools import Image, input_text
from database import Database


class SettingsState(Enum):
    pass


class Base:
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        pg.mouse.set_visible(True)

        self._screen: pg.Surface = screen
        self._padding = padding
        self._font = pg.font.Font(fontname, fontsize)
        self._input_font = pg.font.Font(fontname, 52)
        if not self._states:
            self._states = tuple()
        self._texts = self._init_renders()
        self._block_rect = self._init_block_rect()
        self._texts_rects = self._init_text_rects()
        self._current = 0

        self.game_state = game_state

        self.pressed_keys = False
    
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

    def _change_state(self, events) -> bool:
        change_state = False

        for event in events:
            clicked = False

            if event.type == pg.MOUSEBUTTONDOWN:
                clicked = True

            for idx, rect in enumerate(self._texts_rects):
                if rect.collidepoint(pg.mouse.get_pos()):
                    self._current = idx

                    if clicked:
                        change_state = True

            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_SPACE, pg.K_RETURN]:
                    self.pressed_keys = True
            if self.pressed_keys and event.type == pg.KEYUP:
                if event.key in [pg.K_SPACE, pg.K_RETURN]:
                    change_state = True
                    self.pressed_keys = False

        return change_state

    def draw(self):
        self._screen.fill((0, 0, 0))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE
            text = self._font.render(self._states[idx].value, False, color)
            self._screen.blit(text, rect)


class BeginMenu(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        self._states = tuple(BeginMenuState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

    def update(self, events):
        self.game_state = self.game_state.begin_menu

        if not self._change_state(events):
            return

        match self._states[self._current]:
            case BeginMenuState.login:
                self.game_state = self.game_state.login
            case BeginMenuState.register:
                self.game_state = self.game_state.registration
            case BeginMenuState.exit:
                self.game_state = self.game_state.exit


class Registration(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        self._states = tuple(RegistrState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)
        self.inputing_login = False
        self.inputing_pswrd = False
        self.user_login = 'log'
        self.user_pswrd = 'pswrd'

    def update(self, events, db: Database):
        self.game_state = self.game_state.registration

        if self.inputing_login:
            self.user_login, self.inputing_login = input_text(events, self.user_login, self.inputing_login)
        if self.inputing_pswrd:
            self.user_pswrd, self.inputing_pswrd = input_text(events, self.user_pswrd, self.inputing_pswrd)

        if not self._change_state(events):
            return

        match self._states[self._current]:
            case RegistrState.user_login:
                self.user_login = ''
                self.inputing_pswrd = False
                self.inputing_login = True

            case RegistrState.user_password:
                self.user_pswrd = ''
                self.inputing_login = False
                self.inputing_pswrd = True

            case RegistrState.register:
                if db.new_user(self.user_login, self.user_pswrd):
                    self.game_state = self.game_state.menu
                else:
                    print(DBAutentication.login_error.value)

            case RegistrState.back:
                self.game_state = self.game_state.begin_menu

    def draw(self):
        self._screen.fill((0, 0, 0))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE

            if self._states[idx] == RegistrState.user_login:
                text = self._input_font.render(self.user_login, False, color)
                center = rect.center
                rect = text.get_rect()
                rect.center = center
            elif self._states[idx] == RegistrState.user_password:
                text = self._input_font.render('*' * len(self.user_pswrd), False, color)
                center = rect.center
                rect = text.get_rect()
                rect.center = center
            else:
                text = self._font.render(self._states[idx].value, False, color)

            self._screen.blit(text, rect)


class Login(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        self._states = tuple(LoginState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)
        self.inputing_login = False
        self.inputing_pswrd = False
        self.user_login = 'log'
        self.user_pswrd = 'pswrd'

    def update(self, events, db):
        self.game_state = self.game_state.login

        if self.inputing_login:
            self.user_login, self.inputing_login = input_text(events, self.user_login, self.inputing_login)
        if self.inputing_pswrd:
            self.user_pswrd, self.inputing_pswrd = input_text(events, self.user_pswrd, self.inputing_pswrd)

        if not self._change_state(events):
            return

        match self._states[self._current]:
            case LoginState.user_login:
                self.user_login = ''
                self.inputing_pswrd = False
                self.inputing_login = True

            case LoginState.user_password:
                self.user_pswrd = ''
                self.inputing_login = False
                self.inputing_pswrd = True

            case LoginState.login:
                match db.authentication(self.user_login, self.user_pswrd):
                    case DBAutentication.successful:
                        self.game_state = self.game_state.menu
                    case DBAutentication.login_error:
                        print(DBAutentication.login_error.value)
                    case DBAutentication.pass_error:
                        print(DBAutentication.pass_error.value)

            case LoginState.back:
                self.game_state = self.game_state.begin_menu

    def draw(self):
        self._screen.fill((0, 0, 0))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE

            if self._states[idx] == LoginState.user_login:
                text = self._input_font.render(self.user_login, False, color)
                center = rect.center
                rect = text.get_rect()
                rect.center = center
            elif self._states[idx] == LoginState.user_password:
                text = self._input_font.render('*' * len(self.user_pswrd), False, color)
                center = rect.center
                rect = text.get_rect()
                rect.center = center
            else:
                text = self._font.render(self._states[idx].value, False, color)

            self._screen.blit(text, rect)


class Menu(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 64, fontsize: int = 64):
        self._states = tuple(MenuState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

    def update(self, events, db: Database):
        self.game_state = self.game_state.menu

        if not self._change_state(events):
            return

        match self._states[self._current]:
            case MenuState.play:
                self.game_state = self.game_state.restart
            case MenuState.records:
                print(db.top_score())  # plug
            case MenuState.settings:
                pass
            case MenuState.logout:
                self.game_state = self.game_state.begin_menu
            case MenuState.exit:
                self.game_state = self.game_state.exit


class Records(Base):
    pass


class Pause(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 hero, padding: int = 64, fontsize: int = 64):
        self._states = tuple(PauseState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

        self._blured_surf = Image(surf=self._screen).blur(35).surf
        self._hero = hero

    @property
    def screen(self):
        return

    @screen.setter
    def screen(self, surf: pg.Surface):
        self._blured_surf = Image(surf=surf).blur(35).surf

    def update(self, events, db: Database, user_login):
        if not self._change_state(events):
            self.game_state = self.game_state.pause
            return

        if self._hero.health <= 0:
            score = self._hero.score.score
            if score > db.get_user_score(user_login):
                db.change_score(user_login, score)

        match self._states[self._current]:
            case PauseState.resume:
                if self._hero.health <= 0:
                    return
                self.game_state = self.game_state.play
            case PauseState.restart:
                self.game_state = self.game_state.restart
            case PauseState.exit:
                self.game_state = self.game_state.menu

    def draw(self):
        self._screen.blit(self._blured_surf, (0, 0))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE
            text = self._font.render(self._states[idx].value, False, color)

            if idx == 0 and self._hero.health <= 0:
                text = self._font.render(f"Scored: {self._hero.score.score}",
                                         False, MENU_ACTIVE)
                center = rect.center
                rect = text.get_rect()
                rect.center = center

            self._screen.blit(text, rect)
