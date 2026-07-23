# piece.py

class Piece:
    """
    Represents a chess piece.
    """

    def __init__(self, piece_type, color):
        """
        piece_type: 'P', 'N', 'B', 'R', 'Q', 'K'
        color: 'w' or 'b'
        """
        self.type = piece_type.upper()
        self.color = color

    def __str__(self):
        """
        Print the piece as a single character.
        White = uppercase
        Black = lowercase
        """
        if self.color == "w":
            return self.type
        return self.type.lower()

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        """
        Material value of the piece.
        """
        values = {
            "P": 100,
            "N": 320,
            "B": 330,
            "R": 500,
            "Q": 900,
            "K": 20000
        }
        return values[self.type]

    @property
    def is_white(self):
        return self.color == "w"

    @property
    def is_black(self):
        return self.color == "b"

    @staticmethod
    def color(piece):
        if isinstance(piece, Piece):
            return piece.color
        if isinstance(piece, str) and len(piece) >= 2:
            return piece[0]
        return None

    @staticmethod
    def type(piece):
        if isinstance(piece, Piece):
            return piece.type
        if isinstance(piece, str) and len(piece) >= 2:
            return piece[1].upper()
        return None