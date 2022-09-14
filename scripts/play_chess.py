#--------------------------CS 677 - TERM PROJECT-------------------------#

#-------------------------CHESS MOVE RECOMMENDER-------------------------#

#--------------SCRIPT_TO_PLAY_A_CHESS_GAME_WITH_MODEL--------------------#

# Author : Surendranath Reddy Nagula

import os
import chess
import chess.svg
import chess.pgn
import chess.engine
import pandas as pd
import time
from IPython.display import display
from IPython.display import clear_output
import cloudpickle as cp

# Loading Random Forest model
path = os.getcwd()
print('Current directory: \n',path)
file = 'model.pkl'

with open(file, 'rb') as f:
    rf = cp.load(f)
    
def fen_to_dataframe(fen_list):
    '''Converts a list of FEN strings to a dataframe of positions similar to
    input data. This can be used as test data, for making predictions and playing
    chess moves according to predicted evaluation score
    Inputs: fen_list - list of FEN strings
    Output: dataframe with chess board positions as numeric values
    '''
    
    col_names = {}
    df = pd.DataFrame.from_dict(col_names)
    for fen in fen_list:
        fields = []
        fields.append(fen.split('/'))
        status = fields[0][-1].split(' ')
        ranks = fields[0][:-1] + [status[0]]
        position = []
        for rank in ranks:
            bitboard = ''
            for sq in rank:
                if sq.isnumeric():
                    bitboard += int(sq)*'0'
                else:
                    bitboard += sq
            bitboard = list(bitboard)
            position.append(bitboard)
        position = [sq for p in position for sq in p] + status[1:]
        position = pd.Series(position)
        df = df.append(position, ignore_index = True)
        
    files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    squares = [f + r for r in ranks[::-1] for f in files]

    piece_map = {'r': -5, 'n': -3, 'b': -3, 'q': -9, 'k': -100, 'p': -1, 
                 'R': 5, 'N': 3, 'B': 3, 'Q': 9, 'K': 100, 'P': 1, 0: 0}
    status_cols = {64:'turn_to_play', 65:'castling', 66:'en_passant', 
                   67:'half_move_clock', 68:'full_move_count'}
    turn_map = {'w': 1, 'b': -1}
    
    col_dict = {}
    for i in range(64):
        col_dict[i] = squares[i]
        df[i] = df[i].map(piece_map)
    df[64] = df[64].map(turn_map)
    df = df.fillna(0)
    df = df.rename(columns = col_dict)
    df = df.rename(columns = status_cols)
    df = df.drop(['castling', 'en_passant', 'half_move_clock'], axis = 1)
    
    return df


'''
Initialization - reset to initial board position
Should be run before every game
'''

engine = chess.engine.SimpleEngine.popen_uci("stockfish_13_win_x64_bmi2")
limit = chess.engine.Limit(time=1.0)
# stockfish = 'WHITE'
stockfish = 'BLACK'
current_pos = chess.STARTING_FEN
board = chess.Board(current_pos)
dh = display(board, display_id=True)

'''Play game Stockfish vs ML'''

while True:
    try:
        # Stockfish play
        board = chess.Board(current_pos)
        result = engine.play(board, limit)
        board.push(result.move)
        clear_output()
        display(board)
        time.sleep(0.1)
        current_pos = board.fen()
    
        # ML model play
        legal_moves_view = (str(board.legal_moves).split('(')[1].rstrip(')>')).split(',') 
        legal_move_list = []
        for move in board.legal_moves:
            board = chess.Board(current_pos)
            board.push(move)
            legal_move_list.append((board.fen()))
            board.pop()
        # Convert all possible legal moves to dataframe
        legal_moves_df = fen_to_dataframe(legal_move_list)
        # Obtain evaluation score for each move from random forest model
        pred_scores = rf.predict(legal_moves_df)
        
        # Select move depending on white/ black
        if stockfish == 'BLACK':
            best_move_idx = pred_scores.argmax()
        else:
            best_move_idx = pred_scores.argmin()
        
        # Play the move with best score
        ctr = 0
        board = chess.Board(current_pos)
        for move in board.legal_moves:
            if ctr == best_move_idx:
                board.push(move)
            ctr += 1
        # Display move
        dh.update(board)
        current_pos = board.fen()
        time.sleep(0.3)

    except (KeyError, AttributeError):
        print("\nGame Over! Restart game?")
        break
