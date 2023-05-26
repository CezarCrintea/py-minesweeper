"""Main code of the game"""

import curses
import time
import sys
from field import Field

MESSAGE = 1
TITLE = MESSAGE + 1
CURSOR = TITLE + 1
EMPTY = CURSOR + 1
MASKED = EMPTY + 1
MARKED = MASKED + 1
MINES_1 = MARKED + 1
MINES_2 = MINES_1 + 1
MINES_3 = MINES_2 + 1
MINES_4 = MINES_3 + 1
MINES_5 = MINES_4 + 1
MINES_6 = MINES_5 + 1
MINES_7 = MINES_6 + 1
MINES_8 = MINES_7 + 1


def main(stdscr, args):
    """Main loop of the game"""
    sys.setrecursionlimit(2000)
    setup_curses(stdscr)
    display_welcome_screen(stdscr)

    field_width, field_height, mines_perc = choose_game_type(stdscr)

    field = Field(field_width, field_height, mines_perc)

    display_main_screen(stdscr, field)


def setup_curses(stdscr):
    """Setup curses"""
    stdscr.clear()

    # Enable color mode
    curses.start_color()
    curses.use_default_colors()
    # Hide the cursor
    curses.curs_set(0)

    # Define a pair of custom color
    curses.init_pair(MESSAGE, curses.COLOR_BLUE, -1)
    curses.init_pair(TITLE, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(CURSOR, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(MASKED, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(MARKED, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(EMPTY, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(MINES_1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(MINES_2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(MINES_3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(MINES_4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(MINES_5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(MINES_6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(MINES_7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(MINES_8, curses.COLOR_RED, curses.COLOR_BLACK)


def display_welcome_screen(stdscr):
    """Displays the welcome screen and wait for any key to be pressed"""
    # Get the screen dimensions
    height, width = stdscr.getmaxyx()

    # Coordinates start from top left, in the format of y, x.
    welcome_text = "Welcome to MineSweeper"
    x_pos = int((width - len(welcome_text)) / 2)
    y_pos = int((height - 1) / 2)
    stdscr.addstr(y_pos, x_pos, welcome_text, curses.color_pair(TITLE))

    press_a_key = "Press any key to start."
    stdscr.addstr(
        height - 2, width - len(press_a_key), press_a_key, curses.color_pair(MESSAGE)
    )

    # Actually draws the text above to the positions specified.
    stdscr.refresh()

    # Grabs a value from the keyboard without Enter having to be pressed (see cbreak above)
    stdscr.getch()


def choose_game_type(stdscr) -> tuple[int, int, int]:
    """Displays a screen to choose a minefield size and squares with mines percentage"""

    # Get the screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()

    options = [
        {"text": "Easy", "width": 10, "height": 10, "mines": 7},
        {"text": "Medium", "width": 30, "height": 15, "mines": 14},
        {"text": "Hard", "width": 60, "height": 20, "mines": 21},
    ]

    stdscr.clear()

    # Coordinates start from top left, in the format of y, x.

    textblock_height = 1 + 4 + 2 * len(options)

    prompt_text = "Choose game type"
    x_pos = int((screen_width - len(prompt_text)) / 2)
    y_pos = int((screen_height - textblock_height) / 2)
    stdscr.addstr(y_pos, x_pos, prompt_text, curses.color_pair(TITLE))

    for i, option in enumerate(options):
        opt_text = option["text"]
        opt_w = option["width"]
        opt_h = option["height"]
        opt_mines = option["mines"]
        option_text = f"{i+1}. {opt_text} ({opt_w} x {opt_h} {opt_mines}% mines)"
        stdscr.addstr(y_pos + 4 + 2 * i, x_pos, option_text, curses.color_pair(MESSAGE))

    # Actually draws the text above to the positions specified.
    stdscr.refresh()

    key = stdscr.getch()

    if key == ord("1"):
        selected_option = 0
    elif key == ord("2"):
        selected_option = 1
    elif key == ord("3"):
        selected_option = 2
    else:
        selected_option = 0

    return (
        options[selected_option]["width"],
        options[selected_option]["height"],
        options[selected_option]["mines"],
    )


def display_main_screen(stdscr, field: Field):
    """Displayes the main screen"""

    # Set up the screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)  # Refresh every 100 milliseconds

    # Get the screen dimensions
    screen_height, screen_width = stdscr.getmaxyx()

    # Initial position of the blinking character
    cursor_x = screen_width // 2
    cursor_y = screen_height // 2

    height = field.height
    width = field.width

    min_x = int((screen_width - width) / 2)
    min_y = int((screen_height - height) / 2)
    max_x = min_x + width
    max_y = min_y + height

    display_field(stdscr, field, min_x, min_y, cursor_x, cursor_y)

    # Start the main loop
    while True:
        # Listen for keypresses
        key = stdscr.getch()

        # Clear the screen
        stdscr.clear()

        # Move the character based on the arrow keys
        if key == curses.KEY_UP and cursor_y > min_y:
            cursor_y -= 1
        elif key == curses.KEY_DOWN and cursor_y < max_y - 1:
            cursor_y += 1
        elif key == curses.KEY_LEFT and cursor_x > min_x:
            cursor_x -= 1
        elif key == curses.KEY_RIGHT and cursor_x < max_x - 1:
            cursor_x += 1
        elif key == ord(" "):
            x = cursor_x - min_x
            y = cursor_y - min_y
            field.reveal_square(x, y)
        elif (key == ord("m")) or (key == ord("M")):
            x = cursor_x - min_x
            y = cursor_y - min_y
            field.toggle_mine_marker(x, y)
        elif (key == ord("q")) or (key == ord("Q")):
            break

        display_field(stdscr, field, min_x, min_y, cursor_x, cursor_y)

        # Delay for smoother animation
        time.sleep(0.2)


def display_field(
    stdscr, field: Field, min_x: int, min_y: int, cursor_x: int, cursor_y: int
):
    """Display the field of mines"""

    for y, row in enumerate(field.squares):
        for x, char in enumerate(row):
            crt_y = min_y + y
            crt_x = min_x + x
            square = field.squares[y][x]
            color = MASKED
            displayed_char = char
            if (crt_x == cursor_x) and (crt_y == cursor_y):
                # Draw the blinking character
                stdscr.addstr(crt_y, crt_x, "*", curses.color_pair(CURSOR))
            else:
                if square.mask:
                    displayed_char = " "
                    color = MASKED
                elif square.flag:
                    displayed_char = "*"
                    color = MARKED
                elif square.mines == 0:
                    displayed_char = " "
                    color = EMPTY
                elif (square.mines >= 1) and (square.mines <= 8):
                    displayed_char = str(square.mines)
                    color = MINES_1 + square.mines - 1

                stdscr.addstr(crt_y, crt_x, displayed_char, curses.color_pair(color))
        # Refresh the screen
    stdscr.refresh()


if __name__ == "__main__":
    # Get command-line arguments excluding the script name
    args = sys.argv[1:]

    # Initialize Curses
    curses.wrapper(main, args)
