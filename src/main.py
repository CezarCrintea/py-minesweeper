"""Main code of the game"""

from textual.app import App
from game import Game
from help import Help


class MinesweeperApp(App):
    """The application class"""

    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle Dark Mode")]
    CSS_PATH = [
        "game.css",
        "choose_game_type.css",
        "game_header.css",
        "game_message.css",
        "help.css",
        "mines_grid.css",
    ]
    SCREENS = {"help": Help}

    TITLE = "MineSweeper"

    def on_mount(self) -> None:
        """Show the main screen"""
        self.push_screen(Game())


if __name__ == "__main__":
    app = MinesweeperApp()
    app.run()
