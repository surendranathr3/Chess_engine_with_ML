#--------------------------CS 677 - TERM PROJECT-------------------------#

#-------------------------CHESS MOVE RECOMMENDER-------------------------#

#----------------SCRIPT_TO_EXTRACT_INPUT_DATA_FROM_PGN-------------------#
'''
Script to extract chess board positions from all games in pgn file, 
which can be used as input data for training chess move recommender
'''

# Author : Surendranath Reddy Nagula

import os
import pandas as pd
import chess
import chess.svg
import chess.pgn

path = os.getcwd()
print('Current directory: \n',path)

''' The following pgn contains 880 chess games with each move annotated with an
evaluation score given by Leela Chess Zero chess engine (best engine)'''

pgn = open("./Lc0_0_27_0_w703810_64-bit_4CPU_annotated.pgn")


def pgn_to_input_data(pgn_file):
    '''Reads all games in pgn files and converts them to a dataframe of all
    squares on chessboard with values of pieces on each square. The resultant
    dataframe can be used as input data for training chess move recommender
    Input: pgn file object
    Output: Data frame of chess board positions as numeric values'''

    game_ctr = 0
    col_names = {}
    df = pd.DataFrame.from_dict(col_names)
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break  # end of file
        else:
            print(f'Game {game_ctr}')
            board = game.board()
            fen_list = []
            # Store all moves of a game as FEN strings into a list 
            for move in game.mainline_moves():
                board.push(move)
                fen_list.append(board.fen())
        game_ctr += 1
        
        # Generate dataframe with position-wise (all 64 squares) data
        for fen in fen_list:
            fields = []
            fields.append(fen.split('/'))
            status = fields[0][-1].split(' ')
            ranks = fields[0][:-1] + [status[0]]
            
            '''Converting FEN string to numeric values in order to create a 
            dataframe of board positions'''
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
    
    # Convert categorical columns to numeric by appriopriate mapping & manipulation
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
    return df

# Calling pgn_to_input_data function to get a dataframe with all board positions
df_board_pos = pgn_to_input_data(pgn)
df_board_pos = df_board_pos.drop(['castling', 'en_passant', 'half_move_clock'],
                                 axis = 1)

df_board_pos.to_csv('Chess_input_data.csv')
