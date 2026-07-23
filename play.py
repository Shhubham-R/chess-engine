# play.py

import sys
from board import Board
from move import Move
from search import Search
from move_generator import MoveGenerator

def parse_coordinate(coord):
    """
    Parses chess coordinate (e.g. 'e2') into (row, col).
    """
    if len(coord) != 2:
        return None
    file_char = coord[0].lower()
    rank_char = coord[1]
    
    if not ('a' <= file_char <= 'h') or not ('1' <= rank_char <= '8'):
        return None
        
    col = ord(file_char) - ord('a')
    row = int(rank_char) - 1
    return row, col

def format_coordinate(row, col):
    """
    Formats (row, col) into chess coordinate (e.g. 'e2').
    """
    file_char = chr(ord('a') + col)
    rank_char = str(row + 1)
    return f"{file_char}{rank_char}"

def main():
    print("=" * 40)
    print("          CHESS ENGINE CLI PLAY")
    print("=" * 40)
    print("Enter moves in coordinate format, e.g., 'e2 e4'")
    print("Type 'quit' or 'exit' to stop the game.")
    print("Type 'undo' to take back your last move.")
    print("=" * 40)
    
    board = Board()
    searcher = Search()
    
    while True:
        print("\n" + str(board) + "\n")
        
        if board.turn == 'w':
            # Human's turn
            user_input = input("White to move (your turn): ").strip()
            
            if user_input.lower() in ('quit', 'exit'):
                print("Thanks for playing!")
                break
                
            if user_input.lower() == 'undo':
                if len(board.move_history) >= 2:
                    board.undo_move() # Undo AI move
                    board.undo_move() # Undo Human move
                    print("Undid one full turn.")
                else:
                    print("Nothing to undo.")
                continue
                
            parts = user_input.split()
            if len(parts) != 2:
                print("Invalid input format. Use e.g. 'e2 e4'")
                continue
                
            start = parse_coordinate(parts[0])
            end = parse_coordinate(parts[1])
            
            if not start or not end:
                print("Invalid coordinates. Use letters a-h and numbers 1-8.")
                continue
                
            start_row, start_col = start
            end_row, end_col = end
            
            piece = board.squares[start_row][start_col]
            if piece is None or piece[0] != 'w':
                print("There is no white piece on that starting square.")
                continue
                
            # Make the human move
            move = Move(start_row, start_col, end_row, end_col)
            board.make_move(move)
            print(f"You played: {parts[0]} -> {parts[1]}")
            
        else:
            # AI's turn
            print("Black to move (AI is thinking...)...")
            # depth of 2 search
            ai_move = searcher.find_best_move(board, depth=2)
            
            if ai_move is None:
                print("AI could not find any legal moves.")
                print("Note: This is because move_generator.py piece move methods (pawn_moves, knight_moves, etc.) are currently returning empty lists. You need to implement those rules!")
                # For demo purposes, we will ask user to make a move for Black or switch turn
                input_override = input("Press Enter to skip AI turn, or type 'quit' to exit: ").strip()
                if input_override.lower() in ('quit', 'exit'):
                    break
                board.turn = 'w'
            else:
                board.make_move(ai_move)
                start_coord = format_coordinate(ai_move.start_row, ai_move.start_col)
                end_coord = format_coordinate(ai_move.end_row, ai_move.end_col)
                print(f"AI played: {start_coord} -> {end_coord}")

if __name__ == "__main__":
    main()
