"""Contains the Field class"""

from square import Square


class Field:
    """Contains the information for the whole minefield.
    The minefield has a rectangular shape and is composed of squares."""

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.squares = [[Square() for y in range(width)] for x in range(length)]

    def generate_image(self):
        """Generates the image of the field as string"""
        image_str = [
            [self._generate_square_image(square) for square in row]
            for row in self.squares
        ]
        return image_str

    def _generate_square_image(self, square):
        if square.masked:
            return ""
