"""Contains the square class"""


class Square:
    """Contains the information for a field's square"""

    def __init__(self):
        self.mine = False
        self.mask = True
        self.flag = False
        self.mines = 0

    def toggle_mine_marker(self):
        """Toggles the mine marker on the specified square"""
        self.flag = not self.flag
        self.mask = not self.flag
