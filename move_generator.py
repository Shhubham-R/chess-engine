from piece import Piece


class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def generate_moves(self, color):
        """
        Returns a list of all legal moves for the given color.
        """
        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col]

                if piece == ".":
                    continue

                if Piece.color(piece) != color:
                    continue

                piece_type = Piece.type(piece)

                if piece_type == "P":
                    moves.extend(self.pawn_moves(row, col, piece))

                elif piece_type == "N":
                    moves.extend(self.knight_moves(row, col, piece))

                elif piece_type == "B":
                    moves.extend(self.bishop_moves(row, col, piece))

                elif piece_type == "R":
                    moves.extend(self.rook_moves(row, col, piece))

                elif piece_type == "Q":
                    moves.extend(self.queen_moves(row, col, piece))

                elif piece_type == "K":
                    moves.extend(self.king_moves(row, col, piece))

        return moves

    # ----------------------------------------------------
    # Pawn
    # ----------------------------------------------------

    def pawn_moves(self, row, col, piece):
        return []

    # ----------------------------------------------------
    # Knight
    # ----------------------------------------------------

    def knight_moves(self, row, col, piece):
        return []

    # ----------------------------------------------------
    # Bishop
    # ----------------------------------------------------

    def bishop_moves(self, row, col, piece):
        return []

    # ----------------------------------------------------
    # Rook
    # ----------------------------------------------------

    def rook_moves(self, row, col, piece):
        return []

    # ----------------------------------------------------
    # Queen
    # ----------------------------------------------------

    def queen_moves(self, row, col, piece):
        return (
            self.rook_moves(row, col, piece)
            + self.bishop_moves(row, col, piece)
        )

    # ----------------------------------------------------
    # King
    # ----------------------------------------------------

    def king_moves(self, row, col, piece):
        return []