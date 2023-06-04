"""The choose game type screen module"""

import re
from typing import NamedTuple
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, Button


class GameType(NamedTuple):
    """Game type data"""

    name: str
    width: int
    height: int
    mines_prc: int


class ChooseGameType(ModalScreen[GameType]):
    """The choose game type screen class"""

    game_types = [
        GameType("Easy", 10, 10, 7),
        GameType("Medium", 30, 15, 14),
        GameType("Hard", 60, 20, 21),
    ]

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("Choose game type")
            with Vertical():
                for i, game_type in enumerate(self.game_types):
                    yield Button(
                        label=game_type.name, id=f"game_type_{i}", variant="success"
                    )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handles the game type selection"""
        if event.button.id is None:
            return
        matches = re.findall(r"\d+", event.button.id)
        game_type_id = int(matches[0])
        self.dismiss(self.game_types[game_type_id])
