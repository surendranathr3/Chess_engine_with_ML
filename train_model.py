#--------------------------CS 677 - TERM PROJECT-------------------------#

#-------------------------CHESS MOVE RECOMMENDER-------------------------#

#------------------SCRIPT_TO_TRAIN_MODEL_WITH_DATASET--------------------#

# Author : Surendranath Reddy Nagula

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import cloudpickle as cp

# Loading training data
path = os.getcwd()
print('Current directory: \n',path)
model_path = os.path.join(path, 'model.pkl')
file = 'Chess_training_data.csv'
df_train = pd.read_csv(file, index_col = 0)

# Train Random forest regressor using data
X = df_train.iloc[:,:-1]
Y = df_train.iloc[:,-1:].values.ravel()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3,
                                                    random_state = 40)
regr = RandomForestRegressor(max_depth = 20, random_state = 40)
regr.fit(X_train, Y_train)

# Check training error
pred_scores = regr.predict(X_test)
rmse = round(mean_squared_error(Y_test, pred_scores), 2)
print(f'\nRMSE on training data: {rmse}\n')

with open(model_path, 'wb') as f:
    cp.dump(regr, f)
print('Stored random forest regressor model in file "model.pkl"\n')