import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        # Check if move is in list of valid moves
        board = game_state["board"]
        valid_moves = self.valid_moves(game_state)
        return move in valid_moves


        
    
                


    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
    
        board = game_state["board"]
        turn = game_state["turn"]
        valid_moves = []

        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece == '.' or piece[0] != ('w' if turn == 'white' else 'b'):
                    continue
                player = piece[0]
                piece_type = piece[1]
                directions = []
                
                if piece_type == 'K':  # King (one step in any direction)
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        if 0 <= r < 5 and 0 <= c < 5 and (board[r][c] == '.' or board[r][c][0] != player):
                            valid_moves.append(((row, col), (r, c)))

                elif piece_type == 'Q':  # Queen 
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        while 0 <= r < 5 and 0 <= c < 5:
                            if board[r][c] == '.':
                                valid_moves.append(((row, col), (r, c)))
                            elif board[r][c][0] != player:
                                valid_moves.append(((row, col), (r, c)))
                                break
                            else:
                                break
                            r += dr
                            c += dc

                elif piece_type == 'B':  # Bishop (diagonal)
                    directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        while 0 <= r < 5 and 0 <= c < 5:
                            if board[r][c] == '.':
                                valid_moves.append(((row, col), (r, c)))
                            elif board[r][c][0] != player:
                                valid_moves.append(((row, col), (r, c)))
                                break
                            else:
                                break
                            r += dr
                            c += dc

                elif piece_type == 'N':  # Knight (L-shape moves)
                    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
                    for dr, dc in moves:
                        r, c = row + dr, col + dc
                        if 0 <= r < 5 and 0 <= c < 5 and (board[r][c] == '.' or board[r][c][0] != player):
                            valid_moves.append(((row, col), (r, c)))

                elif piece_type == 'p':  # Pawn 
                    direction = -1 if player == 'w' else 1
                    if 0 <= row + direction < 5 and board[row + direction][col] == '.':
                        valid_moves.append(((row, col), (row + direction, col)))
                    elif 0 <= row + direction < 5 and board[row + direction][col][0] != player:
                        valid_moves.append(((row, col), (row + direction, col)))

        return valid_moves

        

    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end

        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'

        # Check if the pawn reaches the last row, promote to Queen
        if piece[1] == 'p':
            if end_row == 0 and piece[0] == 'w':  
                game_state["board"][end_row][end_col] = piece[0] + 'Q'
                print(f"{piece} promoted to Queen at {chr(ord('A') + end_col)}{5 - end_row}!")
            elif end_row == 4 and piece[0] == 'b':  
                game_state["board"][end_row][end_col] = piece[0] + 'Q'
                print(f"{piece} promoted to Queen at {chr(ord('A') + end_col)}{5 - end_row}!")
            else:
                game_state["board"][end_row][end_col] = piece  # No promotion, just a regular move
        else:
            game_state["board"][end_row][end_col] = piece  # Regular move for other pieces


        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state



    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        
        last_piece_count = sum(1 for row in self.current_game_state["board"] for piece in row if piece != '.')
        no_piece_change_turns = 0
        turn_count = 1
        max_turns_without_capture = 10  # Max turns before draw if no pieces are captured
        
        with open('gameTrace-HH-10.txt', 'w') as log_file:
            log_file.write("Initial Board State:\n")
            for row in self.current_game_state["board"]:
                log_file.write("  ".join(piece.rjust(3) for piece in row) + "\n")
            log_file.write("\n")

            
            while True:
                self.display_board(self.current_game_state)
                player = self.current_game_state["turn"].capitalize()
                print(f"{player} to move (Turn #{turn_count}): ", end='')

                move = input()
                if move.lower() == 'exit':
                    print("Game exited.")
                    exit(1)

                move = self.parse_input(move)
                if not move or not self.is_valid_move(self.current_game_state, move):
                    print("Invalid move. Try again.")
                    continue

                current_piece_count = sum(1 for row in self.current_game_state["board"] for piece in row if piece != '.')

                if current_piece_count == last_piece_count:
                    no_piece_change_turns += 1
                else:
                    no_piece_change_turns = 0  

                last_piece_count = current_piece_count

                start_pos = f"{chr(ord('A') + move[0][1])}{5 - move[0][0]}"  
                end_pos = f"{chr(ord('A') + move[1][1])}{5 - move[1][0]}"   
                move_str = f"move from {start_pos} to {end_pos}"

                log_file.write(f"Turn #{turn_count}: {player} {move_str}\n")

                self.make_move(self.current_game_state, move)

                log_file.write(f"New Board Configuration:\n")
                for row in self.current_game_state["board"]:
                    log_file.write("  ".join(piece.rjust(3) for piece in row) + "\n") 
                log_file.write("\n")

                board = self.current_game_state["board"]
                white_king_found = False
                black_king_found = False

                for row in range(5):
                    for col in range(5):
                        if board[row][col] == 'wK':
                            white_king_found = True
                        if board[row][col] == 'bK':
                            black_king_found = True

                if not white_king_found:
                    winner = "Black"
                    print(f"Game Over. {winner} wins! White's King has been captured.")
                    log_file.write(f"Game Over. {winner} wins! White's King has been captured.\n")
                    break
                elif not black_king_found:
                    winner = "White"
                    print(f"Game Over. {winner} wins! Black's King has been captured.")
                    log_file.write(f"Game Over. {winner} wins! Black's King has been captured.\n")
                    break

                # Check for draw if no pieces were captured for 10 turns
                if no_piece_change_turns >= max_turns_without_capture:
                    print("Game Over. It's a draw! No pieces were captured in 10 turns.\n")
                    log_file.write("Game Over. It's a draw! No pieces were captured in 10 turns.\n")
                    break

                turn_count += 1

if __name__ == "__main__":
    game = MiniChess()
    game.play()