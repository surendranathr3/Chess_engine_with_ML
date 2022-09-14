# Chess engine with Machine Learning


**LIBRARIES TO BE INSTALLED:**

python-chess
pip install python-chess
https://python-chess.readthedocs.io/en/latest/

cloudpickle
pip install cloudpickle
https://pypi.org/project/cloudpickle/

IPython
pip install ipython
https://ipython.org/ipython-doc/3/install/index.html

Common libraries used:
os, re, numpy, pandas, sklearn


**CODE & DATA FILES EXPLAINED:**

###pgn_convert_board_pos_to_input_data.py
- To convert pgn file to a dataframe of chess board positions
- Can be directly run, output csv will be stored in current working directory
Input file: 'Lc0_0_27_0_w703810_64-bit_4CPU_annotated.pgn'
Output file: 'Chess_input_data.csv' 

###pgn_convert_eval_scores_to_label_data.py
- To convert pgn file to a dataframe of position evaluation scores
- Can be directly run, output csv will be stored in current working directory
Input file: 'Lc0_0_27_0_w703810_64-bit_4CPU_annotated.pgn'
Output files: 'Chess_label_data.csv', 'Error_scores.csv'

###data_cleaning.py
- To prepare final dataset from already generated csv files mentioned above
- Can be directly run, output csv will be stored in current working directory
Input files: 'Chess_input_data.csv', 'Chess_label_data.csv', 'Error_scores.csv'
Output file: 'Chess_training_data.csv' 

###train_model.py
- To create and store a random forest model based on the training dataset of chess positions 
- Can be directly run, output model stored as '.pkl'(pickle file) in current working directory
Input files: 'Chess_training_data.csv'
Output file: 'model.pkl' 

###play_chess.py / play_chess.ipynb
- To play chess using the trained model
- To be run preferably with jupyter notebook, chess game can be visualized better in jupyter
Input files: 'model.pkl', 'stockfish_13_win_x64_bmi2.exe'
Output file: None

###stockfish_13_win_x64_bmi2.exe
- This is the stockfish chess engine which can be used to play chess
