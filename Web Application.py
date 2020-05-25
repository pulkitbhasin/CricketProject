#Creating a logistic regression model and creating a streamlit web application

import pandas as pd
import numpy as np
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import streamlit as st

#Reading dataset
battingDataset = pd.read_csv("U-19 World Cup Dataset.csv", index_col=0)


#Storing all data except for predictor variable in dataframe
X = battingDataset.loc[:, battingDataset.columns != 'Played for India']
y = battingDataset.loc[:, battingDataset.columns == 'Played for India']
os_data_X = X
os_data_y = y


#70-30 train-test split and creating a model and testing it; 82% accuracy
columns = ['Runs', 'Balls Faced', 'Strike Rate', '100s', '4s',
       'Wickets Taken', 'Captain']
X = pd.DataFrame(data=os_data_X,columns=columns )
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)


#Function that normalizes data to analyze coefficients
def normalize(df):
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(df)
    df_normalized = pd.DataFrame(x_scaled)
    return df_normalized

#Analyzing coefficients assigned by logistic regression model
two = normalize(y)
one = normalize(X)
import statsmodels.api as sm
logit_model=sm.Logit(two, one)
result=logit_model.fit()
print(result.summary2())


#Implementing streamlit web application
runs = st.text_input('Enter number of runs scored')
ballsFaced = st.text_input("Enter number of balls faced")
strikeRate = st.text_input("Enter your batting strike rate")
centuries = st.text_input("Enter number of 100s scored")
fours = st.text_input("Enter number of boundaries scored")
wicketsTaken = st.text_input("Enter number of wickets taken")
captain = st.text_input("Enter whether you were captain or not : Yes/No")


def model(runs, average, ballsFaced, strikeRate, centuries, fours, wicketsTaken, captain):
    runs = float(runs)
    average = float(average)
    ballsFaced = float(ballsFaced)
    strikeRate = float(strikeRate)
    centuries = float(centuries)
    fours = float(fours)
    wicketsTaken = float(wicketsTaken)
    if captain == "Yes":
        captain = True
    else:
        captain = False
    inputData = [runs, ballsFaced, strikeRate, centuries, fours, wicketsTaken, captain]
    return logreg.predict_proba([inputData])[0][1]


st.write('The probability that this player will make it into the main team is', probability)
