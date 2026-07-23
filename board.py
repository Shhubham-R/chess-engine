class Board:

    def __init__(self):
        self.squares = self._empty_board()
        self.turn = "w"
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []
        self.setup_start_position()

    def make_move(self, move):
        """
        Applies a move to the board and records the state for undoing.
        """
        # Save state to history stack
        squares_copy = [row[:] for row in self.squares]
        state = {
            'squares': squares_copy,
            'turn': self.turn,
            'castling_rights': self.castling_rights.copy(),
            'en_passant_target': self.en_passant_target,
            'halfmove_clock': self.halfmove_clock,
            'fullmove_number': self.fullmove_number
        }
        self.move_history.append(state)

        # Move the piece
        piece = self.squares[move.start_row][move.start_col]
        self.squares[move.end_row][move.end_col] = piece
        self.squares[move.start_row][move.start_col] = None

        # Handle promotion
        if move.promotion:
            self.squares[move.end_row][move.end_col] = self.turn + move.promotion.upper()

        # Update fullmove number and turn
        if self.turn == 'b':
            self.fullmove_number += 1
        self.turn = 'b' if self.turn == 'w' else 'w'

    def undo_move(self):
        """
        Undoes the last move, restoring the board state.
        """
        if not self.move_history:
            return
        state = self.move_history.pop()
        self.squares = state['squares']
        self.turn = state['turn']
        self.castling_rights = state['castling_rights']
        self.en_passant_target = state['en_passant_target']
        self.halfmove_clock = state['halfmove_clock']
        self.fullmove_number = state['fullmove_number']

    def _empty_board(self):
        return [[None for _ in range(8)] for _ in range(8)]

    def setup_start_position(self):
        back_rank = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for file in range(8):
            self.squares[0][file] = 'w' + back_rank[file]
            self.squares[1][file] = 'wP'
            self.squares[6][file] = 'bP'
            self.squares[7][file] = 'b' + back_rank[file]

    def get_piece(self, rank, file):
        return self.squares[rank][file]

    def set_piece(self, rank, file, piece):
        self.squares[rank][file] = piece

    def is_empty(self, rank, file):
        return self.squares[rank][file] is None

    def is_white(self, piece):
        return piece is not None and piece[0] == 'w'

    def is_black(self, piece):
        return piece is not None and piece[0] == 'b'

    def on_board(self, rank, file):
        return 0 <= rank < 8 and 0 <= file < 8

    def __str__(self):
        rows = []
        for rank in range(7, -1, -1):
            row = []
            for file in range(8):
                piece = self.squares[rank][file]
                row.append(piece if piece else '.')
            rows.append(f"{rank + 1}  " + ' '.join(row))
        rows.append("   a  b  c  d  e  f  g  h")
        return '\n'.join(rows)


if __name__ == "__main__":
    b = Board()
    print(b)
