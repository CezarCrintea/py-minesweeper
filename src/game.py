"""The game screen"""

from rich.text import Text
from rich.style import Style

from textual.app import ComposeResult, RenderResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Footer, Label

from field import Field
from choose_game_type import GameType, ChooseGameType

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


class GameHeader(Widget):
    """Header for game. Diplays marked mines and not-marked mines"""

    cleared_squares = reactive(0)
    """int: Keep track of how many squares the player has cleared."""
    total_squares = reactive(0)
    """int: Keep track of how many squares are on the field."""
    marked_mines = reactive(0)
    """int: Keep track of how many mines the player has marked."""
    total_mines = reactive(0)
    """int: Keep track of how many mines are on the field."""

    def compose(self) -> ComposeResult:
        """Compose the game header.

        Returns:
            ComposeResult: The result of composing the game header.
        """
        with Horizontal():
            yield Label(self.app.title, id="app-title")
            yield Label(id="squares")
            yield Label(id="mines")

    def watch_marked_mines(self, new_value: int):
        """Watch the marked_mines reactive and update when it changes.

        Args:
            moves (int): The number of marked mines.
        """
        self.update_mines_label()

    def watch_total_mines(self, new_value: int):
        """Watch the on-count reactive and update when it changes.

        Args:
            filled (int): The number of cells that are currently on.
        """
        self.update_mines_label()

    def update_mines_label(self):
        """Update mines label"""
        self.query_one("#mines", Label).update(
            f"Mines marked {self.marked_mines} of {self.total_mines}"
        )

    def update_squares_label(self):
        """Updates squares label"""
        self.query_one("#squares", Label).update(
            f"Squares cleared {self.cleared_squares} of {self.total_squares}"
        )


class GameMessage(Label):
    """Widget to tell the user they have lost/won."""

    def show(self, won: bool) -> None:
        """Show the end game message.

        Args:
            won (bool): The player has won or not.
        """

        self.update("You won !!!" if won else "You lost!!!")
        self.add_class("visible")

    def hide(self) -> None:
        """Hide the winner message."""
        self.remove_class("visible")


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
            cleared_squares = 0

            for row in self.field.squares:
                for square in row:
                    if not square.mask:
                        cleared_squares += 1

            self.post_message(self.SquareCleared(cleared_squares, self.total_squares))

    def action_mark(self) -> None:
        """Toggles the mine marker for the square under the cursor"""
        self.field.toggle_mine_marker(self.cursor_x, self.cursor_y)

        marked_mines = 0

        for row in self.field.squares:
            for square in row:
                if square.flag:
                    marked_mines += 1

        self.post_message(self.SquareCleared(marked_mines, self.total_mines))

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


class Game(Screen[None]):
    """The welcome screen class"""

    BINDINGS = [
        Binding("n", "new_game", "New Game"),
        Binding("question_mark", "push_screen('help')", "Help", key_display="?"),
        Binding("q", "quit", "Quit"),
    ]

    game_type = reactive[GameType | None]
    field: reactive[Field | None]

    def compose(self) -> ComposeResult:
        yield GameHeader()
        yield MinesGrid()
        yield Footer()
        yield GameMessage()

    def game_playable(self, playable: bool) -> None:
        """Mark the game as playable, or not.

        Args:
            playable (bool): Should the game currently be playable?
        """
        self.query_one(MinesGrid).active = playable

    def action_new_game(self) -> None:
        """Start a new game."""

        def type_choosen(game_type_choosen: GameType) -> None:
            """Called when ChooseGameType is dismissed."""
            self.game_type = game_type_choosen

            self.field = Field(
                self.game_type.width, self.game_type.height, self.game_type.mines_prc
            )

            self.query_one(GameHeader).marked_mines = 0
            self.query_one(GameMessage).hide()

            mines_grid = self.query_one(MinesGrid)
            mines_grid.field = self.field
            mines_grid.cursor_x = self.field.width // 2
            mines_grid.cursor_y = self.field.height // 2

            self.game_playable(True)

        self.app.push_screen(ChooseGameType(), type_choosen)
        self.game_playable(False)

    def on_mount(self) -> None:
        self.action_new_game()
