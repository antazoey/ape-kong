from ape_kong.game import Action, Character


class TestCharacter:
    MAX_Y = 10
    MAX_X = 10
    PIECE = "APE"

    def create_char(self, y=0, x=0, piece=None):
        piece = piece or self.PIECE
        return Character(y, x, piece)

    def test_handle_left_when_cannot_go_left(self):
        x = len(self.PIECE) - 1
        character = self.create_char(x=x)
        character.handle_action(Action.MOVE_LEFT, self.MAX_Y, self.MAX_X)

        # Assert that the piece did not move
        assert character.x == x
        assert character.y == 0

    def test_handle_left(self):

        # Initialize at the first spot on the first line,
        # with exactly room for two pieces (enough to move left once)
        character = self.create_char(x=len(self.PIECE))
        character.handle_action(Action.MOVE_LEFT, self.MAX_Y, self.MAX_X)

        # Assert that we moved back into the 0th position
        assert character.x == 0
        assert character.y == 0

    def test_handle_right_when_cannot_go_right(self):
        x = self.MAX_X - 2
        character = self.create_char(x=x)
        character.handle_action(Action.MOVE_RIGHT, self.MAX_Y, self.MAX_X)

        # Assert that the piece did not move
        assert character.x == x
        assert character.y == 0

    def test_handle_right(self):

        # Initialize at the last spot on the first line,
        # with exactly room for two pieces (enough to move left once)
        length_of_two_pieces = len(self.PIECE) * 2
        min_spot = self.MAX_X - length_of_two_pieces + 1

        character = self.create_char(x=min_spot)
        character.handle_action(Action.MOVE_RIGHT, self.MAX_Y, self.MAX_X)

        # Assert that we moved back into the 0th position
        expected_x = (self.MAX_X - len(self.PIECE)) + 1
        assert character.x == expected_x
        assert character.y == 0

    def test_handle_up_when_cannot_go_up(self):
        character = self.create_char()
        character.handle_action(Action.MOVE_UP, self.MAX_Y, self.MAX_X)
        assert character.x == 0
        assert character.y == 0

    def test_handle_up(self):
        character = self.create_char(y=1)
        character.handle_action(Action.MOVE_UP, self.MAX_Y, self.MAX_X)
        assert character.x == 0
        assert character.y == 0

    def test_handle_down_when_cannot_go_down(self):
        character = self.create_char(y=self.MAX_Y)
        character.handle_action(Action.MOVE_DOWN, self.MAX_Y, self.MAX_X)
        assert character.x == 0
        assert character.y == self.MAX_Y

    def test_handle_down(self):
        character = self.create_char(y=self.MAX_Y - 1)
        character.handle_action(Action.MOVE_DOWN, self.MAX_Y, self.MAX_X)
        assert character.x == 0
        assert character.y == self.MAX_Y
