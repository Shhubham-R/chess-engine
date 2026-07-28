# app.py

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from board import Board
from search import Search
from move import Move
from move_generator import MoveGenerator
from evaluation import Evaluation
from piece import Piece
import threading

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

board_lock = threading.Lock()
board = Board()
searcher = Search()

def format_coordinate(row, col):
    """Formats (row, col) into chess coordinate (e.g. 'e2')."""
    file_char = chr(ord('a') + col)
    rank_char = str(row + 1)
    return f"{file_char}{rank_char}"

def get_board_state_serialized():
    squares_serialized = []
    for r in range(8):
        row_pieces = []
        for c in range(8):
            piece = board.squares[r][c]
            if piece is None:
                row_pieces.append(None)
            else:
                row_pieces.append({
                    'type': Piece.type(piece),
                    'color': Piece.color(piece)
                })
        squares_serialized.append(row_pieces)
    
    # Generate all legal moves for the active player
    raw_moves = MoveGenerator.generate_moves(board)
    legal_moves_serialized = []
    for m in raw_moves:
        legal_moves_serialized.append({
            'start_row': m.start_row,
            'start_col': m.start_col,
            'end_row': m.end_row,
            'end_col': m.end_col,
            'promotion': m.promotion
        })

    eval_score = Evaluation.evaluate(board)

    # Format history as strings
    history_serialized = []
    for m in board.played_moves:
        start_coord = format_coordinate(m.start_row, m.start_col)
        end_coord = format_coordinate(m.end_row, m.end_col)
        promo = f"={m.promotion}" if m.promotion else ""
        history_serialized.append(f"{start_coord}{end_coord}{promo}")

    return {
        'squares': squares_serialized,
        'turn': board.turn,
        'evaluation': eval_score,
        'legal_moves': legal_moves_serialized,
        'history': history_serialized,
        'game_over': len(raw_moves) == 0
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    with board_lock:
        return jsonify(get_board_state_serialized())

@app.route('/api/move', methods=['POST'])
def make_move_api():
    data = request.json
    start_row = data.get('start_row')
    start_col = data.get('start_col')
    end_row = data.get('end_row')
    end_col = data.get('end_col')
    promotion = data.get('promotion') # e.g. 'q'

    with board_lock:
        if board.turn != 'w':
            return jsonify({'error': "It is not White's turn."}), 400

        # Generate moves
        legal_moves = MoveGenerator.generate_moves(board)
        matched_move = None
        for m in legal_moves:
            if (m.start_row == start_row and m.start_col == start_col and
                m.end_row == end_row and m.end_col == end_col):
                if promotion:
                    if m.promotion and m.promotion.lower() == promotion.lower():
                        matched_move = m
                        break
                else:
                    matched_move = m
                    break

        if not matched_move:
            return jsonify({'error': "Invalid or illegal move."}), 400

        # Make human move
        board.make_move(matched_move)
        human_played = {
            'start_row': matched_move.start_row,
            'start_col': matched_move.start_col,
            'end_row': matched_move.end_row,
            'end_col': matched_move.end_col,
            'promotion': matched_move.promotion
        }

        # Make AI move (Black)
        ai_played = None
        if board.turn == 'b':
            ai_move = searcher.find_best_move(board, depth=3)
            if ai_move:
                board.make_move(ai_move)
                ai_played = {
                    'start_row': ai_move.start_row,
                    'start_col': ai_move.start_col,
                    'end_row': ai_move.end_row,
                    'end_col': ai_move.end_col,
                    'promotion': ai_move.promotion
                }

        state = get_board_state_serialized()
        state['human_move'] = human_played
        state['ai_move'] = ai_played
        return jsonify(state)

@app.route('/api/undo', methods=['POST'])
def undo_api():
    with board_lock:
        # Undo both the AI move and the human move
        if len(board.move_history) >= 2:
            board.undo_move() # Undo AI
            board.undo_move() # Undo human
        elif len(board.move_history) == 1:
            board.undo_move() # Undo human
        return jsonify(get_board_state_serialized())

@app.route('/api/reset', methods=['POST'])
def reset_api():
    with board_lock:
        global board
        board = Board()
        return jsonify(get_board_state_serialized())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
