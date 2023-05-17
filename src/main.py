"""Main code of the game"""

import curses
import sys


def main(stdscr, args):
    """Main loop of the game"""

    setup_curses(stdscr)
    display_welcome_screen(stdscr)


def setup_curses(stdscr):
    stdscr.clear()

    # Enable color mode
    curses.start_color()
    curses.use_default_colors()
    # Hide the cursor
    curses.curs_set(0)

    # Define a pair of custom color
    curses.init_pair(1, curses.COLOR_BLUE, -1)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)


def display_welcome_screen(stdscr):
    # Get the screen dimensions
    height, width = stdscr.getmaxyx()

    # Coordinates start from top left, in the format of y, x.
    welcome_text = "Welcome to MineSweeper"
    x_pos = int((width - len(welcome_text)) / 2)
    y_pos = int((height - 1) / 2)
    stdscr.addstr(y_pos, x_pos, welcome_text, curses.color_pair(2))

    press_a_key = "Press any key to start."
    stdscr.addstr(
        height - 2, width - len(press_a_key), press_a_key, curses.color_pair(1)
    )

    # Actually draws the text above to the positions specified.
    stdscr.refresh()

    # Grabs a value from the keyboard without Enter having to be pressed (see cbreak above)
    stdscr.getch()


if __name__ == "__main__":
    # Get command-line arguments excluding the script name
    args = sys.argv[1:]

    # Initialize Curses
    curses.wrapper(main, args)
