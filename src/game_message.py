from textual.widgets import Label


class GameMessage(Label):
    """Widget to tell the user they have lost/won."""

    def show(self, won: bool) -> None:
        """Show the end game message.

        Args:
            won (bool): The player has won or not.
        """
        if won:
            self.update("You won !!!")
            self.add_class("won")
        else:
            self.update("You lost!!!")
            self.add_class("lost")

        self.add_class("visible")

    def hide(self) -> None:
        """Hide the winner message."""
        self.remove_class("visible")
        self.remove_class("won")
        self.remove_class("lost")
