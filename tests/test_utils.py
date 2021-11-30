from ape_kong.utils import get_clear_space

TEXT = "APEX"


def test_get_clear_space_left():
    start_x = 8
    new_x = 6

    actual_start_x, actual_length = get_clear_space(0, 0, start_x, new_x, TEXT)

    assert actual_start_x == 10
    assert actual_length == 2


def test_get_clear_space_right():
    start_x = 6
    new_x = 8

    actual_start_x, actual_length = get_clear_space(0, 0, start_x, new_x, TEXT)

    assert actual_start_x == 6
    assert actual_length == 2
