# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 17:17:24 2018

@author: nikhil741
"""
import numpy as np
import pandas as pd

## READ TRAIN file GENERATED FROM feautre_extractor.py FILE  #######
train_df = pd.read_csv("./output/train.csv")
X_train = train_df.iloc[:, :-1].values
y_train = train_df.iloc[:, -1].values

##### read test file generated from feautre_extractor.py file  ############
test_df = pd.read_csv("./output/test.csv")
X_test = test_df.iloc[:, :-1].values

###########  HANDELING THE MISSING DATA  ###############################
#Find columns having na value
train_df.columns[train_df.isna().any()].tolist()

##########  MEAN ON NAN VALUE TO EXPENSE  ################################
from sklearn.preprocessing import Imputer
imputer_expense = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imputer_expense = imputer_expense.fit(X_train[:, 4:5])
X_train[:, 4:5] = imputer_expense.transform(X_train[:, 4:5])
X_test[:, 4:5] = imputer_expense.transform(X_test[:, 4:5])

##########  MOST FREQUNET HOLDIAY VALUES TO NAN HOLIDAYS VALUE  ##############
imputer_holiday = Imputer(missing_values = 'NaN', strategy = 'most_frequent', axis = 0)
imputer_holiday = imputer_holiday.fit(X_train[:, 5:6])
X_train[:, 5:6] = imputer_holiday.transform(X_train[:, 5:6])
X_test[:, 5:6] = imputer_holiday.transform(X_test[:, 5:6])

######TRAINING DATA ##############################3
###  ENCODE THE COUNTRY TO NUMERICAL DATA  ######
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X_train[:, 3] = labelencoder_X.fit_transform(X_train[:, 3])

### ONE HOT ENCODE THE COUNTRY TRAIN DATA  ######
onehotencoder = OneHotEncoder(categorical_features = [3])
X_train = onehotencoder.fit_transform(X_train).toarray()

#Avoiding dummy variable trap
X_train = X_train[:, 1:]

########### TRANSFORM TESTING DATA  #################################3
#TRANSFORM THE TESTTING DATA ACCORDINGLY LEARNED FROM TRAINING DATA  ##########
X_test[:, 3] = labelencoder_X.transform(X_test[:, 3])
X_test = onehotencoder.transform(X_test).toarray()
#Avoiding dummy variable trap
X_test = X_test[:, 1:]

###########  CALCULATE SMAPE VALUE  ################
def smape(y_actual, y_pred):
    return (100/(y_pred.shape[0]))*(np.sum(np.abs(np.subtract(y_actual, y_pred)))/((np.sum(np.add(y_actual, y_pred)))/2))


####### APPLYING THE MODEL  ################################
from sklearn.ensemble import RandomForestRegressor
regr = RandomForestRegressor(n_estimators=10000, max_depth=12, random_state=0)
regr.fit(X_train, y_train)
y_pred_train = regr.predict(X_train)
y_pred_test = regr.predict(X_test)
smape(y_train, y_pred_train)

######## GENERATE THE SUBMISSIONS FILE IN REQUIRED FORMAT  ###############
sales_df = pd.DataFrame({'Sales':y_pred_test})
submission_df = test_df[['S_No', 'Year', 'Month', 'Product_ID', 'Country']]
submission_df = submission_df.join(sales_df)
submission_df.to_csv("./output/yds_submission2018.csv", index=False)