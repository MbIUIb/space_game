from enum import Enum
from time import time

import pygame as pg

from config import BeginMenuState, RegistrState, LoginState, MenuState, RecordsState, PauseState, DBAutentication, MENU_NONACTIVE, MENU_ACTIVE, screen_width, SELF_NAME
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
        self.error_font = pg.font.Font(fontname, 30)
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
        self.error = ''
        self.error_time = 0

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
                    self.error = 'this login is already occupied'
                    self.error_time = time()

            case RegistrState.back:
                self.game_state = self.game_state.begin_menu

    def draw(self):
        self._screen.fill((0, 0, 0))

        if self.error:
            if time() - self.error_time < 5:
                _score_surf = self.error_font.render(f'{self.error}', True, MENU_NONACTIVE)
                _score_rect = _score_surf.get_rect(center=(screen_width//2, 50))
                self._screen.blit(_score_surf, _score_rect)

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
        self.error = ''
        self.error_time = 0

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
                        self.error = DBAutentication.login_error.value
                        self.error_time = time()
                    case DBAutentication.pass_error:
                        self.error = DBAutentication.pass_error.value
                        self.error_time = time()

            case LoginState.back:
                self.game_state = self.game_state.begin_menu

    def draw(self):
        self._screen.fill((0, 0, 0))

        if self.error:
            if time() - self.error_time < 5:
                _score_surf = self.error_font.render(f'{self.error}', True, MENU_NONACTIVE)
                _score_rect = _score_surf.get_rect(center=(screen_width//2, 50))
                self._screen.blit(_score_surf, _score_rect)

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
                self.game_state = self.game_state.records
            case MenuState.settings:
                pass
            case MenuState.logout:
                self.game_state = self.game_state.begin_menu
            case MenuState.exit:
                self.game_state = self.game_state.exit


class Records(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 padding: int = 30, fontsize: int = 30):
        self._states = tuple(RecordsState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

    def update(self, events):
        self.game_state = self.game_state.records

        if not self._change_state(events):
            return

        match self._states[self._current]:
            case RecordsState.back:
                self.game_state = self.game_state.menu

    def draw(self, db: Database, login):
        self._screen.fill((0, 0, 0))
        user_name = login
        user_score = db.get_user_score(user_name)
        top_score = db.top_score()

        for (name, _) in top_score:
            if user_name == name:
                self_bar = 'you in top 10!!!'.center(65)
                user_score = ''
                break
            else:
                self_bar = user_name

        top_score.append((user_name, user_score))

        for idx, (text, rect) in enumerate(zip(self._texts, self._texts_rects)):
            color = MENU_ACTIVE if idx == self._current else MENU_NONACTIVE
            text = self._font.render(self._states[idx].value, False, color)

            if idx < len(RecordsState.__members__.values())-1:
                if idx == 10:
                    text = self._font.render(f"{self_bar}", False, SELF_NAME)
                    score_text = self._font.render(f"{user_score}", False, SELF_NAME)
                else:
                    if user_name == top_score[idx][0]:
                        color = SELF_NAME
                    else:
                        color = MENU_ACTIVE
                    name = top_score[idx][0] if len(top_score[idx][0]) < 25 else top_score[idx][0][:22]+'...'
                    score = str(top_score[idx][1]) if len(str(top_score[idx][1])) < 10 else str(top_score[idx][1])[:8]+'..'
                    text = self._font.render(f"{str(idx+1)}. {name}", False, color)
                    score_text = self._font.render(f"{score}", False, color)
                center = rect.center
                rect = text.get_rect(midleft=(50,center[1]))
                score_rect = text.get_rect(midleft=(screen_width-170, center[1]))
                self._screen.blit(score_text, score_rect)

            self._screen.blit(text, rect)


class Pause(Base):
    def __init__(self, fontname: str, game_state, screen: pg.Surface,
                 hero, padding: int = 64, fontsize: int = 64):
        self._states = tuple(PauseState.__members__.values())
        super().__init__(fontname, game_state, screen, padding, fontsize)

        self._blured_surf = Image(surf=self._screen).blur(35).surf
        self._hero = hero
        self.save_score = False

    @property
    def screen(self):
        return

    @screen.setter
    def screen(self, surf: pg.Surface):
        self._blured_surf = Image(surf=surf).blur(35).surf

    def update(self, events, db: Database, user_login):
        if self._hero.health <= 0 and not self.save_score:
            self.save_score = True
            score = self._hero.score.score
            if score > db.get_user_score(user_login):
                db.change_score(user_login, score)

        if not self._change_state(events):
            self.game_state = self.game_state.pause
            return

        match self._states[self._current]:
            case PauseState.resume:
                if self._hero.health <= 0:
                    return
                self.game_state = self.game_state.play
            case PauseState.restart:
                self.save_score = False
                self.game_state = self.game_state.restart
            case PauseState.exit:
                self.save_score = False
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
