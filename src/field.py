"""Contains the Field class"""

from square import Square


class Field:
    """Contains the information for the whole minefield.
    The minefield has a rectangular shape and is composed of squares."""

    def __init__(self, width: int, height: int, mines_perc: int):
        self.width = width
        self.height = height
        self.mines_perc = mines_perc
        self.game_over = False
        self.setup_minefield()

    def setup_minefield(self):
        """Setup the minefield"""
        self.squares = [
            [Square() for x in range(self.width)] for y in range(self.height)
        ]
        self.plant_mines()
        self.setup_mine_count()

    def plant_mines(self):
        """Plant the mines"""
        self.squares[0][0].mine = True
        self.squares[5][3].mine = True
        self.squares[9][0].mine = True
        self.squares[7][7].mine = True

    def setup_mine_count(self):
        """Setup the mine count for every square"""
        for y, row in enumerate(self.squares):
            for x, square in enumerate(row):
                if square.mine:
                    square.mines = -1
                    continue
                square.mines = 0
                if x > 0 and y > 0:
                    if self.squares[y - 1][x - 1].mine:
                        square.mines += 1
                if x > 0:
                    if self.squares[y][x - 1].mine:
                        square.mines += 1
                if x > 0 and y < self.height - 1:
                    if self.squares[y + 1][x - 1].mine:
                        square.mines += 1
                if y < self.height - 1:
                    if self.squares[y + 1][x].mine:
                        square.mines += 1
                if x < self.width - 1 and y < self.height - 1:
                    if self.squares[y + 1][x + 1].mine:
                        square.mines += 1
                if x < self.width - 1:
                    if self.squares[y][x + 1].mine:
                        square.mines += 1
                if x < self.width - 1 and y > 0:
                    if self.squares[y - 1][x + 1].mine:
                        square.mines += 1
                if y > 0:
                    if self.squares[y - 1][x].mine:
                        square.mines += 1

    def reveal_square(self, x: int, y: int):
        """
        Reveal the specified square, if masked.
        If there is a mine on that square sets game over.
        If the square is empty, reveals recursively the adjacent squares without mines.
        """
        square = self.squares[y][x]
        if not square.mask:
            return

        square.mask = False

        if square.mine:
            self.game_over = True

        if square.mines > 0:
            return

        if x > 0 and y > 0:
            if not self.squares[y - 1][x - 1].mine:
                self.reveal_square(x - 1, y - 1)
        if x > 0:
            if not self.squares[y][x - 1].mine:
                self.reveal_square(x - 1, y)
        if x > 0 and y < self.height - 1:
            if not self.squares[y + 1][x - 1].mine:
                self.reveal_square(x - 1, y + 1)
        if y < self.height - 1:
            if not self.squares[y + 1][x].mine:
                self.reveal_square(x, y + 1)
        if x < self.width - 1 and y < self.height - 1:
            if not self.squares[y + 1][x + 1].mine:
                self.reveal_square(x + 1, y + 1)
        if x < self.width - 1:
            if not self.squares[y][x + 1].mine:
                self.reveal_square(x + 1, y)
        if x < self.width - 1 and y > 0:
            if self.squares[y - 1][x + 1].mine:
                self.reveal_square(x + 1, y - 1)
        if y > 0:
            if self.squares[y - 1][x].mine:
                self.reveal_square(x, y - 1)

    def toggle_mine_marker(self, x: int, y: int):
        """Toggles the mine marker on the specified square"""
        square = self.squares[y][x]
        square.toggle_mine_marker()
