# evaluation.py

from piece import Piece

# Piece-Square Tables (PST) from White's perspective.
# Positive values encourage placing pieces on these squares.
# For Black, we flip the row index: 7 - row.

PAWN_PST = [
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [ 50,  50,  50,  50,  50,  50,  50,  50],
    [ 10,  10,  20,  30,  30,  20,  10,  10],
    [  5,   5,  10,  25,  25,  10,   5,   5],
    [  0,   0,   0,  20,  20,   0,   0,   0],
    [  5,  -5, -10,   0,   0, -10,  -5,   5],
    [  5,  10,  10, -20, -20,  10,  10,   5],
    [  0,   0,   0,   0,   0,   0,   0,   0]
]

KNIGHT_PST = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20,   0,   0,   0,   0, -20, -40],
    [-30,   0,  10,  15,  15,  10,   0, -30],
    [-30,   5,  15,  20,  20,  15,   5, -30],
    [-30,   0,  15,  20,  20,  15,   0, -30],
    [-30,   5,  10,  15,  15,  10,   5, -30],
    [-40, -20,   0,   5,   5,   0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

BISHOP_PST = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-10,   0,   5,  10,  10,   5,   0, -10],
    [-10,   5,   5,  10,  10,   5,   5, -10],
    [-10,   0,  10,  10,  10,  10,   0, -10],
    [-10,  10,  10,  10,  10,  10,  10, -10],
    [-10,   5,   0,   0,   0,   0,   5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

ROOK_PST = [
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  5,  10,  10,  10,  10,  10,  10,   5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [  0,   0,   0,   5,   5,   0,   0,   0]
]

QUEEN_PST = [
    [-20, -10, -10,  -5,  -5, -10, -10, -20],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-10,   0,   5,   5,   5,   5,   0, -10],
    [ -5,   0,   5,   5,   5,   5,   0,  -5],
    [  0,   0,   5,   5,   5,   5,   0,  -5],
    [-10,   5,   5,   5,   5,   5,   0, -10],
    [-10,   0,   5,   0,   0,   0,   0, -10],
    [-20, -10, -10,  -5,  -5, -10, -10, -20]
]

KING_PST = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [ 20,  20,   0,   0,   0,   0,  20,  20],
    [ 20,  30,  10,   0,   0,  10,  30,  20]
]

class Evaluation:
    """
    Evaluates a chess position using material values and Piece-Square Tables (PST).
    
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
        'K': 20000
    }

    @staticmethod
    def evaluate(board):
        """
        Returns a comprehensive evaluation score for the current board state.
        """
        score = 0

        for r in range(8):
            for c in range(8):
                piece = board.squares[r][c]
                if piece is None or piece == ".":
                    continue

                kind = Piece.type(piece)
                color = Piece.color(piece)

                if kind not in Evaluation.PIECE_VALUES:
                    continue

                # 1. Material Value
                val = Evaluation.PIECE_VALUES[kind]

                # 2. Positional Value (PST)
                pst_row = r if color == 'w' else 7 - r
                pst_val = 0
                
                if kind == 'P':
                    pst_val = PAWN_PST[pst_row][c]
                elif kind == 'N':
                    pst_val = KNIGHT_PST[pst_row][c]
                elif kind == 'B':
                    pst_val = BISHOP_PST[pst_row][c]
                elif kind == 'R':
                    pst_val = ROOK_PST[pst_row][c]
                elif kind == 'Q':
                    pst_val = QUEEN_PST[pst_row][c]
                elif kind == 'K':
                    pst_val = KING_PST[pst_row][c]

                total_value = val + pst_val

                if color == 'w':
                    score += total_value
                else:
                    score -= total_value

        return score