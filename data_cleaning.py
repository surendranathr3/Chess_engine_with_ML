#--------------------------CS 677 - TERM PROJECT-------------------------#

#-------------------------CHESS MOVE RECOMMENDER-------------------------#

#---------------SCRIPT_TO_CLEAN_AND_CREATE_FINAL_DATASET-----------------#

# Author : Surendranath Reddy Nagula

import os
import pandas as pd

# Loading already generated input and label data
path = os.getcwd()
print('Current directory: \n',path)

file_1 = 'Chess_input_data.csv'
file_2 = 'Chess_label_data.csv'
file_3 = 'Error_scores.csv'

df_inputs = pd.read_csv(file_1, index_col = 0)
df_labels = pd.read_csv(file_2, index_col = 0)
df_errors = pd.read_csv(file_3, index_col = 0)

# Dropping rows which contain error scores
drop_list = df_errors['0'].to_list()
df_inputs = df_inputs.drop(df_inputs.index[drop_list])

# Dropping rows upto 10th ply (5th move) since there are no eval scores available
df_inputs.drop(df_inputs[(df_inputs['full_move_count'] == 6) & 
                         (df_inputs.shift(1)['full_move_count'] == 5)].index, inplace = True)
df_inputs = df_inputs.loc[df_inputs['full_move_count'] > 5]

# Changing value of King
df_inputs = df_inputs.replace(4.0, 100.0)
df_inputs = df_inputs.replace(-4.0, -100.0)

df_inputs['score'] = df_labels['score']

# Dropping rows with alpha characters and converting scores column to numeric
df_inputs = df_inputs[~df_inputs['score'].str.contains("[a-zA-Z]").fillna(False)]
df_inputs['score'] = pd.to_numeric(df_inputs['score'], errors='coerce')

# Dropping NaN values and resetting index
df_inputs = df_inputs.dropna(axis=0)
df_inputs = df_inputs.reset_index(drop = True)

df_inputs.to_csv('Chess_training_data.csv')

