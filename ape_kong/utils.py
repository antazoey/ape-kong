from typing import Tuple


def get_clear_space(original_y, new_y, original_x, new_x, text) -> Tuple[int, int]:
    if original_x < new_x:
        # Moved right
        start_x = original_x
        length = new_x - original_x

    elif original_x > new_x:
        # Moved left
        start_x = new_x + len(text)
        length = original_x - new_x

    else:
        start_x = original_x
        length = len(text)

    return start_x, length
