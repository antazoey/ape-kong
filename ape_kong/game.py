import curses
from enum import Enum
from typing import Optional, Tuple


class Action(Enum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_LEFT = 2
    MOVE_RIGHT = 3
    QUIT = 4

    @classmethod
    def from_user_input(cls, user_input: int) -> Optional["Action"]:
        key = None
        if user_input == curses.KEY_UP:
            key = cls.MOVE_UP
        elif user_input == curses.KEY_DOWN:
            key = cls.MOVE_DOWN
        elif user_input == curses.KEY_LEFT:
            key = cls.MOVE_LEFT
        elif user_input == curses.KEY_RIGHT:
            key = cls.MOVE_RIGHT
        elif user_input == "x":
            key = cls.QUIT

        if key:
            return Action(key)


class ActionResult(Enum):
    HAS_MOVED = 0


class Character:
    def __init__(self, y, x, piece):
        self.y = int(y)
        self.x = int(x)
        self.piece = piece.encode("utf8")

    def __iter__(self):
        yield self.y
        yield self.x
        yield self.piece

    def __len__(self):
        return len(self.piece)

    def handle_action(
        self, action: Action, max_y: int, max_x: int
    ) -> Optional[ActionResult]:
        if not action:
            return None

        if action == Action.MOVE_UP and self.y > 0:
            self.y -= 1
        elif action == Action.MOVE_DOWN and self.y < max_y:
            self.y += 1
        elif action == Action.MOVE_LEFT and self.x >= len(self):
            self.x -= len(self)
        elif action == Action.MOVE_RIGHT and self.x <= (max_x - 2 * len(self)) + 1:
            self.x += len(self)
        else:
            return None

        return ActionResult.HAS_MOVED


class ApeKong:
    def __init__(self, window, piece):
        self._window = window
        self.setup()
        screen_height, screen_width = self.screen_size
        self._character = Character(screen_height / 2, screen_width / 2, piece)
        self.draw_ape()

    @property
    def screen_size(self) -> Tuple[float, float]:
        y, x = self._window.getmaxyx()
        return y, x

    def run(self) -> int:
        try:
            while True:
                key = self._window.getch()
                action = Action.from_user_input(key)

                if action == Action.QUIT:
                    break

                original_y = self._character.y
                original_x = self._character.x
                result = self._character.handle_action(action, *self.screen_size)
                if result and result == result.HAS_MOVED:
                    did_draw = self.draw_ape()
                    if did_draw:
                        self.clear(original_y, original_x)

            return 0
        except Exception:
            return 1

    def setup(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self._window.bkgd(" ", curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE)

    def draw_ape(self):
        max_y, max_x = self.screen_size

        self._draw(*self._character)
        return True
        # # Only draw if the character is not going off the screen.
        # if 0 <= self._character.y <= max_y and 0 <= self._character.x <= max_x:
        #     self._draw(*self._character)
        #     return True
        #
        # return False

    def clear(self, y, x):
        spaces = len(self._character) * " "
        self._draw(y, x, spaces)

    def _draw(self, y, x, text):
        max_y, max_x = self.screen_size
        y_is_valid = 0 < y < max_y
        x_is_valid = x >= 0 and x + len(text) - 1 < max_x

        if y_is_valid and x_is_valid:
            self._window.addstr(y, x, text)


def play(piece) -> int:
    def play_ape_kong(window):
        game = ApeKong(window, piece)
        return game.run()

    return curses.wrapper(play_ape_kong)
