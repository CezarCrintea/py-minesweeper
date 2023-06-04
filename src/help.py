"""Help screen"""

from pathlib import Path
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Markdown


class Help(Screen):
    """The help screen for the application."""

    BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]
    """Bindings for the help screen."""

    def compose(self) -> ComposeResult:
        """Compose the game's help.

        Returns:
            ComposeResult: The result of composing the help screen.
        """
        yield Markdown(Path(__file__).with_suffix(".md").read_text())
