# search.py

from evaluation import Evaluation
from move_generator import MoveGenerator


class Search:

    def __init__(self):
        self.nodes = 0

    def find_best_move(self, board, depth):
        """
        Returns the best move for the side to move.
        """

        best_move = None

        if board.turn == 'w':
            best_score = float("-inf")

            for move in MoveGenerator.generate_moves(board):

                board.make_move(move)

                score = self.minimax(
                    board,
                    depth - 1,
                    float("-inf"),
                    float("inf"),
                    False
                )

                board.undo_move()

                if score > best_score:
                    best_score = score
                    best_move = move

        else:
            best_score = float("inf")

            for move in MoveGenerator.generate_moves(board):

                board.make_move(move)

                score = self.minimax(
                    board,
                    depth - 1,
                    float("-inf"),
                    float("inf"),
                    True
                )

                board.undo_move()

                if score < best_score:
                    best_score = score
                    best_move = move

        return best_move

    def minimax(self, board, depth, alpha, beta, maximizing):

        self.nodes += 1

        if depth == 0:
            return Evaluation.evaluate(board)

        moves = MoveGenerator.generate_moves(board)

        # No legal moves
        if not moves:
            return Evaluation.evaluate(board)

        if maximizing:

            value = float("-inf")

            for move in moves:

                board.make_move(move)

                value = max(
                    value,
                    self.minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False
                    )
                )

                board.undo_move()

                alpha = max(alpha, value)

                if beta <= alpha:
                    break

            return value

        else:

            value = float("inf")

            for move in moves:

                board.make_move(move)

                value = min(
                    value,
                    self.minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        True
                    )
                )

                board.undo_move()

                beta = min(beta, value)

                if beta <= alpha:
                    break

            return value