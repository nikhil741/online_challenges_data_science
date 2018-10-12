#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 01:52:30 2018

@author: user
"""
# -*- coding: utf-8 -*-
## IMPORT LIBRARIES ##
import numpy as np
import pandas as pd
from pandas import DataFrame

## FOR SPYDER:: CLEARS ALL VARIABLE
def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]

### READ TRAIN FILE
train_df = pd.read_csv("./dataset/yds_train2018.csv")

### GROUP BY TRAIN_DF ########
train_group = train_df.groupby(by=['Product_ID', 'Country', 'Year', 'Month'])

## SUMMATION OF SALES OF EACH WEEK OF GIVEN PRODUCT ID, COUNTRY ETC ###########
### LIST_OF_LIST LIKE DATAFRAME WHERE EACH ROW IS DATA AND COLUMNS ARE FIELD VALUES ###
list_of_list = []
for name, group in train_group:
    sum = 0
    for sale in group['Sales']:
        sum += sale
    row = []
    row.append(name[0])
    row.append(name[1])
    row.append(name[2])
    row.append(name[3])
    row.append(sum)
    print(row)
    list_of_list.append(row)


## SALARY IS CUMMALATIVE SUM OF ALL WEEKS FOR A MONTH FOR COUNTRY YEAR AND MONTH ##
## CREATE NEW DATAFRAME ##
headers = ['Product_ID', 'Country', 'Year', 'Month', 'Sales']
train_df = DataFrame(list_of_list, columns=headers)


################################# Handeling Promotional File  ###########################################################
## READ CSV FILE ##
promotion_df = pd.read_csv("./dataset/promotional_expense.csv")
promotion_df = promotion_df.rename(columns={'Product_Type': 'Product_ID'})
## LEFT OUTER JOIN ON TWO DATAFRAMES ##
train_df = pd.merge(train_df, promotion_df, how='left', on=['Product_ID', 'Country', 'Year', 'Month'])
train_df['Year'].dtype
train_df['Country'].dtype
train_df['Month'].dtype

################################## Handeling Holidays File ###############################################
holidays_df = pd.read_excel("./dataset/holidays.xlsx")
holidays_group = holidays_df.groupby(by=['Country'])
country_year_month_date_list = []
for name, group in holidays_group:
    print(group)
    
    for date in group['Date']:
        print(date)
        y_m_d = date.split(',')
        temp = []
        temp.append(name)
        temp.append(y_m_d[0])
        temp.append(y_m_d[1])
        country_year_month_date_list.append(temp)
    print(country_year_month_date_list)

## HOLIDAYS DATAFRAME ##
## HOLIDAYS COLUMN --> NUMBER OF HOLIDAYS IN MONTH FOR GIVEN YEAR MONTH AND COUNTRY
headers = ['Country', 'Year', 'Month']
holidays_df = DataFrame(country_year_month_date_list, columns=headers) 
holidays_df = holidays_df.groupby(holidays_df.columns.tolist()).size().reset_index().rename(columns={0:'Holidays'})

## PRINT DATA TYPES OF EACH COLUMN AND CHANGE ACCORDINGLY TO MATCH GIVEN DATA
holidays_df['Year'].dtype
holidays_df['Country'].dtype
holidays_df['Month'].dtype

## CONVERT YEAR AND MONTH FIELD VALUE TO TYPE INT TO MATCH THE TRAIN DATASET ##
holidays_df['Year']=holidays_df['Year'].apply(int)
holidays_df['Month']=holidays_df['Month'].apply(int)


#################### MERGE TWO DATAFRAMES  ############################################
train_df = pd.merge(train_df, holidays_df, how='left', on=['Country', 'Year', 'Month'])

### Maintain Order of Columns in Findal_train_df dataframe
train_df = train_df[['Year', 'Month', 'Product_ID', 'Country', 'Expense_Price', 'Holidays', 'Sales']]
train_df.to_csv("./output/train.csv", encoding='utf-8', index=False)

############ HANDELING THE TEST DATA  ###########################################
##### Reading test data  #################
test_df = pd.read_csv("./dataset/yds_test2018.csv")
##PromotionLEFT OUTER JOIN ON TWO DATAFRAMES ##
test_df = pd.merge(test_df, promotion_df, how='left', on=['Product_ID', 'Country', 'Year', 'Month'])
##Holidays: Left Outer Join MERGE TWO DATAFRAMES  ############################################
test_df = pd.merge(test_df, holidays_df, how='left', on=['Country', 'Year', 'Month'])
#Maintain Order of Columns in Findal_train_df dataframe
test_df = test_df[['Year', 'Month', 'Product_ID', 'Country', 'Expense_Price', 'Holidays', 'S_No']]
test_df.to_csv("./output/test.csv", encoding='utf-8', index=False)