#--------------------------CS 677 - TERM PROJECT-------------------------#

#-------------------------CHESS MOVE RECOMMENDER-------------------------#

#----------------SCRIPT_TO_EXTRACT_LABEL_DATA_FROM_PGN-------------------#
'''
Script to extract evaluation scores from pgn file, which can be used as
label data for training chess move recommender
'''

# Author : Surendranath Reddy Nagula

import os
import re
import numpy as np
import pandas as pd
import chess
import chess.svg
import chess.pgn

path = os.getcwd()
print('Current directory: \n',path)

''' The following pgn contains 880 chess games with each move annotated with an
evaluation score given by Leela Chess Zero chess engine (best engine)'''

pgn = open("./Lc0_0_27_0_w703810_64-bit_4CPU_annotated.pgn")

def pgn_extract_scores(pgn_file):
    '''Function to extract eval scores from all moves in all games from a 
    pgn file and create a data frame with a column of scores. The resultant
    dataframe can be used as label data for training chess move recommender
    Input: pgn file object
    Output: Tuple with data frame of eval scores & list of error scores
    '''
    
    game_ctr, total_move_ctr = 0, 0
    error_scores = {}
    col_names = {}
    df = pd.DataFrame.from_dict(col_names)
    # Read each game in pgn file and extract Leela Chess evaluation scores
    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break  # end of file
        else:
            print(f'Game {game_ctr}')
            score_list = []
            game_move_ctr = 0
            # Extract numeric score for each move in game using reg exp filter
            for node in game.mainline():
                '''Excluding scores from first 10 moves in each game since they
                are played from a database, not by evaluation, so no scores given'''
                if game_move_ctr >= 10:
                    score = re.findall(r'.+(?=/)', node.comment)
                    if score:
                        score_list.append(score[0])
                    else:
                        # print(node.uci())
                        error_scores[total_move_ctr] = score
                game_move_ctr += 1
                total_move_ctr += 1
        # Appending each numeric evaluation score into a dataframe
        df = pd.concat([df, pd.Series(score_list)], ignore_index = True)
        game_ctr += 1
    df = df.rename(columns={0:'score'})
    # print(total_move_ctr)
    # print(error_scores)
    return (df, error_scores.keys())

# Calling pgn_extract_scores function to get a dataframe with all scores
df_scores, error_scores = pgn_extract_scores(pgn)

'''Error scores to keep track of moves which are incorrect, the same need to 
be excluded in the input data for training'''
df_error_scores = pd.Series(list(error_scores), dtype = np.int64)

# Exporting data to csv files
df_scores.to_csv('Chess_label_data.csv')
df_error_scores.to_csv('Error_scores.csv')
