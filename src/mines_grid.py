"""The mines_grid module"""

from rich.text import Text
from rich.style import Style

from textual.app import RenderResult
from textual.binding import Binding
from textual.events import Click, MouseMove
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget

from field import Field

CURSOR = 1
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
MINE = MINES_8 + 1


class MinesGrid(Widget, can_focus=True):
    """The main playable grid of game cells."""

    class SquareCleared(Message):
        """Mines marked changed message"""

        def __init__(self, cleared: int, total: int) -> None:
            self.cleared = cleared
            self.total = total
            super().__init__()

    class MineMarked(Message):
        """Mines marked changed message"""

        def __init__(self, marked: int, total: int) -> None:
            self.marked = marked
            self.total = total
            super().__init__()

    class MineExploded(Message):
        """A mine exploded"""

    class FieldCleared(Message):
        """The field was cleared"""

    BINDINGS = [
        Binding("up", "move_up", "Move Up", False),
        Binding("down", "move_down", "Move Down", False),
        Binding("left", "move_left", "Move Left", False),
        Binding("right", "move_right", "Move Right", False),
        Binding("m", "mark", "mark", False),
        Binding("space", "clear", "Toggle", False),
    ]

    field = reactive(Field(10, 10, 7), layout=True)
    active = reactive(False)
    cursor_x = reactive(0)
    cursor_y = reactive(0)

    def __init__(self) -> None:
        self.total_mines = 0
        self.total_squares = 0

        super().__init__()

    def render(self) -> RenderResult:
        if not self.active:
            return Text("")

        styles = {
            CURSOR: Style(color="red", blink=True, bold=True),
            MASKED: Style(color="white", bgcolor="white"),
            MARKED: Style(color="red", bgcolor="white"),
            EMPTY: Style(color="white", bgcolor="black"),
            MINES_1: Style(color="green", bgcolor="black"),
            MINES_2: Style(color="green", bgcolor="black"),
            MINES_3: Style(color="yellow", bgcolor="black"),
            MINES_4: Style(color="yellow", bgcolor="black"),
            MINES_5: Style(color="yellow", bgcolor="black"),
            MINES_6: Style(color="red", bgcolor="black"),
            MINES_7: Style(color="red", bgcolor="black"),
            MINES_8: Style(color="red", bgcolor="black"),
            MINE: Style(color="red", bgcolor="black"),
        }

        field_text = Text("")
        for y, row in enumerate(self.field.squares):
            if y > 0:
                field_text.append("\n")
            for x, square in enumerate(row):
                cell_text = Text(" ")
                if (x == self.cursor_x) and (y == self.cursor_y):
                    # Draw the current position
                    cell_text = Text("*", style=styles[CURSOR])
                else:
                    if square.mask:
                        cell_text = Text(" ", style=styles[MASKED])
                    elif square.flag:
                        cell_text = Text("*", style=styles[MARKED])
                    elif square.mine:
                        cell_text = Text("*", style=styles[MINE])
                    elif square.mines == 0:
                        cell_text = Text(" ", style=styles[EMPTY])
                    elif (square.mines >= 1) and (square.mines <= 8):
                        displayed_char = str(square.mines)
                        color = MINES_1 + square.mines - 1
                        cell_text = Text(displayed_char, style=styles[color])

                field_text.append(cell_text)

        return field_text

    def action_move_up(self) -> None:
        """Moves the cursor up, if possible"""
        if self.cursor_y > 0:
            self.cursor_y -= 1

    def action_move_down(self) -> None:
        """Moves the cursor down, if possible"""
        if self.cursor_y < self.field.height - 1:
            self.cursor_y += 1

    def action_move_left(self) -> None:
        """Moves the cursor left, if possible"""
        if self.cursor_x > 0:
            self.cursor_x -= 1

    def action_move_right(self) -> None:
        """Moves the cursor right, if possible"""
        if self.cursor_x < self.field.width - 1:
            self.cursor_x += 1

    def action_clear(self) -> None:
        """Clear the square under the cursor"""
        self.field.reveal_square(self.cursor_x, self.cursor_y)
        if self.field.mine_exploded:
            self.post_message(self.MineExploded())
        else:
            self.count_cleared_squares_and_send_notification()

    def action_mark(self) -> None:
        """Toggles the mine marker for the square under the cursor"""
        self.field.toggle_mine_marker(self.cursor_x, self.cursor_y)
        self.count_marked_mines_and_send_notification()
        self.count_cleared_squares_and_send_notification()

    def on_click(self, event: Click):
        """Clears or marks the square depending on the button clicked"""
        self.cursor_x = event.x
        self.cursor_y = event.y

        # Left-click to clear
        if event.button == 1:
            self.action_clear()
        # Right click to mark
        elif event.button == 3:
            self.action_mark()

    def on_mouse_move(self, event: MouseMove):
        """Moves the cursor following the movements of the mouse"""
        self.cursor_x = event.x
        self.cursor_y = event.y

    def watch_field(self, new_value: Field):
        """Watch the field reactive and update total squares and mines when it changes.

        Args:
            new_value (int): The new value of field.
        """
        self.total_squares = self.field.width * self.field.height

        total_mines = 0

        for row in self.field.squares:
            for square in row:
                if square.mine:
                    total_mines += 1

        self.total_mines = total_mines

        self.post_message(self.SquareCleared(0, self.total_squares))
        self.post_message(self.MineMarked(0, self.total_mines))

    def count_cleared_squares_and_send_notification(self):
        """Counts the cleared squares and send notification message"""
        cleared_squares = 0

        for row in self.field.squares:
            for square in row:
                if not square.mask:
                    cleared_squares += 1

        self.post_message(self.SquareCleared(cleared_squares, self.total_squares))

        if cleared_squares == self.total_squares:
            self.post_message(self.FieldCleared())

    def count_marked_mines_and_send_notification(self):
        """Counts the marked mines and send nitification message"""
        marked_mines = 0

        for row in self.field.squares:
            for square in row:
                if square.flag:
                    marked_mines += 1

        self.post_message(self.MineMarked(marked_mines, self.total_mines))
