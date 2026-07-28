from piece import Piece
from move import Move


class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def generate_moves(self, color=None, check_legality=True):
        """
        Returns a list of all legal moves. Can be called as:
          - MoveGenerator.generate_moves(board)
          - generator.generate_moves(color)
        """
        if color is None:
            # Called as MoveGenerator.generate_moves(board) where 'self' is the board
            board = self
            generator = MoveGenerator(board)
            return generator.generate_moves(board.turn)

        pseudolegal_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col]

                if piece is None or piece == ".":
                    continue

                if Piece.color(piece) != color:
                    continue

                piece_type = Piece.type(piece)

                if piece_type == "P":
                    pseudolegal_moves.extend(self.pawn_moves(row, col, piece))

                elif piece_type == "N":
                    pseudolegal_moves.extend(self.knight_moves(row, col, piece))

                elif piece_type == "B":
                    pseudolegal_moves.extend(self.bishop_moves(row, col, piece))

                elif piece_type == "R":
                    pseudolegal_moves.extend(self.rook_moves(row, col, piece))

                elif piece_type == "Q":
                    pseudolegal_moves.extend(self.queen_moves(row, col, piece))

                elif piece_type == "K":
                    pseudolegal_moves.extend(self.king_moves(row, col, piece))

        if not check_legality:
            return pseudolegal_moves

        # Filter out moves that leave own king in check
        legal_moves = []
        for m in pseudolegal_moves:
            self.board.make_move(m)
            if not self.is_in_check(color):
                legal_moves.append(m)
            self.board.undo_move()

        return legal_moves

    def is_in_check(self, color):
        """
        Returns True if the king of the given color is currently in check.
        """
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.board.squares[r][c]
                if piece and Piece.type(piece) == 'K' and Piece.color(piece) == color:
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        king_row, king_col = king_pos
        opponent_color = 'b' if color == 'w' else 'w'

        for r in range(8):
            for c in range(8):
                piece = self.board.squares[r][c]
                if piece and Piece.color(piece) == opponent_color:
                    piece_type = Piece.type(piece)
                    opp_moves = []
                    
                    if piece_type == "P":
                        opp_moves = self.pawn_moves(r, c, piece)
                    elif piece_type == "N":
                        opp_moves = self.knight_moves(r, c, piece)
                    elif piece_type == "B":
                        opp_moves = self.bishop_moves(r, c, piece)
                    elif piece_type == "R":
                        opp_moves = self.rook_moves(r, c, piece)
                    elif piece_type == "Q":
                        opp_moves = self.queen_moves(r, c, piece)
                    elif piece_type == "K":
                        opp_moves = self.king_moves(r, c, piece)

                    for m in opp_moves:
                        if m.end_row == king_row and m.end_col == king_col:
                            return True
        return False

    # ----------------------------------------------------
    # Pawn
    # ----------------------------------------------------

    def pawn_moves(self, row, col, piece):
        moves = []
        color = Piece.color(piece)
        direction = 1 if color == 'w' else -1
        start_row = 1 if color == 'w' else 6
        promo_row = 7 if color == 'w' else 0

        # 1 step forward
        next_row = row + direction
        if self.board.on_board(next_row, col) and self.board.is_empty(next_row, col):
            if next_row == promo_row:
                for promo in ['Q', 'R', 'B', 'N']:
                    moves.append(Move(row, col, next_row, col, promotion=promo))
            else:
                moves.append(Move(row, col, next_row, col))
            
            # 2 steps forward from starting rank
            two_next_row = row + 2 * direction
            if row == start_row and self.board.on_board(two_next_row, col) and self.board.is_empty(two_next_row, col):
                moves.append(Move(row, col, two_next_row, col))

        # Captures
        for col_offset in [-1, 1]:
            target_col = col + col_offset
            if self.board.on_board(next_row, target_col):
                target_piece = self.board.squares[next_row][target_col]
                if target_piece and Piece.color(target_piece) != color:
                    if next_row == promo_row:
                        for promo in ['Q', 'R', 'B', 'N']:
                            moves.append(Move(row, col, next_row, target_col, promotion=promo))
                    else:
                        moves.append(Move(row, col, next_row, target_col))
        return moves

    # ----------------------------------------------------
    # Knight
    # ----------------------------------------------------

    def knight_moves(self, row, col, piece):
        moves = []
        color = Piece.color(piece)
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for r_off, c_off in offsets:
            r, c = row + r_off, col + c_off
            if self.board.on_board(r, c):
                target_piece = self.board.squares[r][c]
                if target_piece is None or Piece.color(target_piece) != color:
                    moves.append(Move(row, col, r, c))
        return moves

    # ----------------------------------------------------
    # Bishop
    # ----------------------------------------------------

    def bishop_moves(self, row, col, piece):
        moves = []
        color = Piece.color(piece)
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.board.on_board(r, c):
                target_piece = self.board.squares[r][c]
                if target_piece is None:
                    moves.append(Move(row, col, r, c))
                elif Piece.color(target_piece) != color:
                    moves.append(Move(row, col, r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

    # ----------------------------------------------------
    # Rook
    # ----------------------------------------------------

    def rook_moves(self, row, col, piece):
        moves = []
        color = Piece.color(piece)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.board.on_board(r, c):
                target_piece = self.board.squares[r][c]
                if target_piece is None:
                    moves.append(Move(row, col, r, c))
                elif Piece.color(target_piece) != color:
                    moves.append(Move(row, col, r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

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
        moves = []
        color = Piece.color(piece)
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if self.board.on_board(r, c):
                target_piece = self.board.squares[r][c]
                if target_piece is None or Piece.color(target_piece) != color:
                    moves.append(Move(row, col, r, c))
        return moves