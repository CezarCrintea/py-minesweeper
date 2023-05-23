"""Contains the Field class"""

from square import Square


class Field:
    """Contains the information for the whole minefield.
    The minefield has a rectangular shape and is composed of squares."""

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.game_over = False
        self.setup_minefield()

    def setup_minefield(self):
        """Setup the minefield"""
        self.squares = [
            [Square() for y in range(self.width)] for x in range(self.length)
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
                if x > 0 and y < self.length - 1:
                    if self.squares[y + 1][x - 1].mine:
                        square.mines += 1
                if y < self.length - 1:
                    if self.squares[y + 1][x].mine:
                        square.mines += 1
                if x < self.width - 1 and y < self.length - 1:
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

    def generate_image(self):
        """Generates the image of the field as string"""
        image_str = [
            [self._generate_square_image(square) for square in row]
            for row in self.squares
        ]
        return image_str

    def reveal_square(self, x, y):
        """
        Reveal the specified square, if masked
        If there is a mine on that square sets game over.
        """
        square = self.squares[y][x]
        if not square.mask:
            return

        square.mask = False

        if square.mine:
            self.game_over = True

    def _generate_square_image(self, square):
        if square.mask:
            return "M"
        elif square.mine:
            return "*"
        else:
            return str(square.mines)
