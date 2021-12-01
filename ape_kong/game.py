import curses
from enum import Enum
from random import randint
from typing import Optional, Tuple

from .utils import get_clear_space

HEADER_HEIGHT = 3
BRIDGE_PIECE = "."


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
    def __init__(self, y, x, piece, map):
        self.y = int(y)
        self.x = int(x)
        self.piece = piece.encode("utf8")
        self.map = map

    def __iter__(self):
        yield self.y
        yield self.x
        yield self.piece

    def __len__(self):
        return len(self.piece)

    def handle_action(self, action: Action, max_y: int, max_x: int) -> Optional[Tuple[ActionResult, str]]:
        if not action:
            return None

        original_y = self.y
        original_x = self.x
        new_y = original_y
        new_x = original_x

        if action == Action.MOVE_UP and self.y > HEADER_HEIGHT:
            new_y = self.y - 1
        elif action == Action.MOVE_DOWN and self.y < max_y - 1:
            new_y = self.y + 1
        elif action == Action.MOVE_LEFT and self.x >= len(self):
            new_x = self.x - 1
        elif action == Action.MOVE_RIGHT and (self.x + len(self) - 1) < (max_x - 1):
            new_x = self.x + 1
        else:
            return None

        new_space = (new_y, new_x)
        piece_consumed = MapSquare.NEGATIVE
        map_piece = self.map.get(new_space)
        if map_piece and map_piece != MapSquare.NEGATIVE:
            self.y = new_y
            self.x = new_x
            piece_consumed = map_piece

        if self.x != original_x or self.y != original_y:
            # Prevents going to the same space twice.
            self.map[new_space] = MapSquare.NEGATIVE

        result = ActionResult.HAS_MOVED if self.x != original_x or self.y != original_y else None
        return result, piece_consumed


class MapSquare:
    BRIDGE = BRIDGE_PIECE
    NEGATIVE = " "
    BOMB = "*"


class ApeKong:
    def __init__(self, window, piece):
        self._window = window
        self.setup()
        self.score = 0
        self.draw_score()

        self.map = {}
        character_start_y, character_start_x = self.draw_map()

        self._character = Character(character_start_y, character_start_x, piece, self.map)
        self.draw_character()

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
                result, piece = self._character.handle_action(action, *self.screen_size)
                if result and result == result.HAS_MOVED:
                    self.draw_character()
                    self.score += 1 if piece == MapSquare.BRIDGE else -10
                    self.draw_score()
                    self.clear_old_character_spot(original_y, original_x)

            return 0
        except Exception:
            return 1

    def setup(self):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self._window.bkgd(" ", curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE)

    def draw_character(self):
        self._draw(*self._character)

    def draw_score(self):
        self._draw(0, 0, f"Score: {self.score}")
        self._draw_line(2)

    def draw_map(self) -> Tuple[int, int]:
        screen_height, screen_width = self.screen_size
        screen_height = int(screen_height)
        screen_width = int(screen_width)
        turn_right = True
        index_a = randint(0, screen_width)
        character_start_y = randint(HEADER_HEIGHT, screen_height)
        character_start_x = None  # Gets set in for loop
        for y in range(HEADER_HEIGHT, screen_height):
            index_b = randint(index_a if turn_right else 0, screen_width if turn_right else index_a)
            begin_bridge = min(index_a, index_b)
            end_bridge = max(index_a, index_b)
            is_booster_row = y % 3 == 0
            booster_index = randint(begin_bridge, end_bridge) if is_booster_row else -1
            for i in range(begin_bridge, end_bridge):
                piece = (
                    MapSquare.BOMB if is_booster_row and i == booster_index else MapSquare.BRIDGE
                )
                self.map[(y, i)] = piece
                self._draw(y, i, piece)

            # If this is the pre-selected character start row
            # select the character start column.
            if y == character_start_y:
                character_start_x = randint(begin_bridge, end_bridge)

            # Fill in rest of line with NEGATIVE
            for x in range(0, screen_width):
                if (y, x) not in self.map:
                    self.map[(y, x)] = MapSquare.NEGATIVE

            # Start the next line at the ending of this line.
            # And go the opposite direction.
            index_a = index_b
            turn_right = not turn_right

        return character_start_y, character_start_x

    def clear_old_character_spot(self, original_y, original_x):
        start_x, length = get_clear_space(
            original_y, self._character.y, original_x, self._character.x, self._character.piece
        )
        self._draw(original_y, start_x, " " * length)

    def _draw_line(self, y):
        _, screen_width = self.screen_size

        for i in range(0, int(screen_width)):
            self._draw(y, i, "-")

    def _draw(self, y, x, text):
        max_y, max_x = self.screen_size
        y_is_valid = 0 <= y < max_y
        x_is_valid = x >= 0 and x + len(text) - 1 < max_x

        if y_is_valid and x_is_valid:
            self._window.addstr(y, x, text)


def play(piece) -> int:
    def play_ape_kong(window):
        game = ApeKong(window, piece)
        return game.run()

    return curses.wrapper(play_ape_kong)
