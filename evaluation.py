# evaluation.py

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
        'K': 0
    }

    @staticmethod
    def evaluate(board):
        """
        Returns an evaluation score for the current board.
        """

        score = 0

        for row in board.squares:
            for piece in row:

                if piece is None:
                    continue

                value = Evaluation.PIECE_VALUES[piece.kind.upper()]

                if piece.color == 'w':
                    score += value
                else:
                    score -= value

        return score