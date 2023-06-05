"""The game_header module."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label


class GameHeader(Widget):
    """Header for game. Displays marked mines and not-marked mines."""

    active = reactive(False)
    """bool: True when playing, False otherwise."""
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

    def watch_active(self, new_value: bool):
        """Watch the active reactive and hide/show the labels when it changes."""

        self.update_mines_label()
        self.update_squares_label()

    def watch_cleared_squares(self, new_value: int):
        """Watch the cleared_squares reactive and update the squares label when it changes.

        Args:
            moves (int): The number of cleared squares.
        """
        self.update_squares_label()

    def watch_total_squares(self, new_value: int):
        """Watch the total squares reactive and update the squares label when it changes.

        Args:
            filled (int): The number of cells that are currently on.
        """
        self.update_squares_label()

    def watch_marked_mines(self, new_value: int):
        """Watch the marked_mines reactive and update the label when it changes.

        Args:
            moves (int): The number of marked mines.
        """
        self.update_mines_label()

    def watch_total_mines(self, new_value: int):
        """Watch the total mines reactive and update the label when it changes.

        Args:
            filled (int): The number of cells that are currently on.
        """
        self.update_mines_label()

    def update_mines_label(self):
        """Update mines label"""
        text = (
            f"Mines marked {self.marked_mines} of {self.total_mines}"
            if self.active
            else ""
        )
        self.query_one("#mines", Label).update(text)

    def update_squares_label(self):
        """Updates squares label"""
        text = (
            f"Squares cleared {self.cleared_squares} of {self.total_squares}"
            if self.active
            else ""
        )
        self.query_one("#squares", Label).update(text)
