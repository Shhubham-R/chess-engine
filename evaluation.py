# evaluation.py

from piece import Piece

class Evaluation:
    """
    Evaluates a chess position.

    Positive score  -> White is better
    Negative score  -> Black is better
    """

    # Piece values
    PIECE_VALUES = {
        'P': 100,
        'N': 320,
        'B': 330,
        'R': 500,
        'Q': 900,
        'K': 20000 # Give King a high value
    }

    @staticmethod
    def evaluate(board):
        """
        Returns an evaluation score for the current board.
        """

        score = 0

        for row in board.squares:
            for piece in row:

                if piece is None or piece == ".":
                    continue

                kind = Piece.type(piece)
                color = Piece.color(piece)

                if kind not in Evaluation.PIECE_VALUES:
                    continue

                value = Evaluation.PIECE_VALUES[kind]

                if color == 'w':
                    score += value
                else:
                    score -= value

        return score