#Libraries Required
import pandas as pd
import datetime
import matplotlib as mplt
from matplotlib import dates
import matplotlib.pyplot as plt
import numpy as np 
import math as mt
from datetime import timedelta

#Given Data
N = 100000
W = 0.2
Basket_initial = 1
data = {'BMW'    : [73.69, 73.32, 50.85, 74.15, 84.69, 93.2],
        'Diageo' : [2810 , 3114, 2842.5, 2952, 3402.5, 3878],
        'Nestle' : [83.5 , 104.3, 104.92, 103.68, 110.44, 122.76],
        'Nike' : [71.12 , 93.05, 92.95, 132.98, 133.27, 174.88],
        'Visa' : [133.37 , 181.66, 193.86, 203.88, 226.44, 200.86]
}
Date = [datetime.date(2019,11,27), datetime.date(2019,11,27), datetime.date(2020,5,27), datetime.date(2020,11,27), datetime.date(2021,5,27), datetime.date(2021,11,26)]

#Variable Initialization
Share_performace = []
Basket = []
Redeemed = []
testredemeed = []
Underlying_shares = ""
Redemption_Date = ""
Redeemed_Amount = 0

#Defining the dataframe
df1 = pd.DataFrame(data)

#Performance Share Calculation, Basket Calculation
for i in range(1, 6):

    Share_initail = df1.iloc[0][i-1]
    Share_final = df1.iloc[-1][i-1]
    Share_performace.append(((Share_final/Share_initail)-1)*100)
    Basket.append((Share_final/Share_initail) * W)

    #Calculating basket, shares initial, final and performance
Share_min = min(Share_performace)
Share_min_index = Share_performace.index(Share_min)
WO_Share_initial = df1.iloc[0][Share_min_index]
WO_Share_final = df1.iloc[-1][Share_min_index]
Basket_final = sum(Basket)

#Printing the variables
print(f"The Worst Performing Share is : {df1.columns[Share_min_index]}")
print(f"And WO Share initial is : {WO_Share_initial}")
print(f"And WO Share final is : {WO_Share_final}")

#Calculating Redeem Amounts
for i in range(1, 6):

    for n in range(1, 5):
        
        if df1.iloc[n][i-1] >= (0.85 * df1.iloc[0][i-1]):
            Underlying_shares = df1.columns[i-1]
            Redemption_Date = Date[n]
            Redeemed_Amount = N * (1.0525 + n*0.0525)
        
        elif WO_Share_final >= (0.85 * WO_Share_initial):
            Underlying_shares = df1.columns[i-1]
            Redemption_Date = Date[-1]
            Redeemed_Amount = N * 1.315
            
        elif Basket_final > (0.85 * Basket_initial):
            Underlying_shares = df1.columns[i-1]
            Redemption_Date = Date[-1]
            Redeemed_Amount = N * 1.00
            
        else:
            Underlying_shares = df1.columns[i-1]
            Redemption_Date = Date[-1]
            Redeemed_Amount = N * ( 1.00 + (WO_Share_final - 0.85 * WO_Share_initial)/WO_Share_initial)
            
        Redeemed.append({'Underlying Shares' : Underlying_shares, 'Redemption Date' : Redemption_Date, 'Redeemed Amount' : Redeemed_Amount})

#Pivoting and Sorting the DataFrame (df)
df2 = pd.DataFrame(Redeemed)
df3 = df2.pivot_table(index=['Redemption Date'], values = ['Redeemed Amount'], aggfunc='count').reset_index()
Prob = df3.sort_values(by=['Redemption Date', 'Redeemed Amount'], ascending=[True, False])

#Normalizing Count of each date to find their normalized probability, sotring the results in PROB array
for i in range (1,5):
    Prob['Redeemed Amount'] = Prob['Redeemed Amount'] /Prob['Redeemed Amount'] .abs().sum()
Prob.rename(columns = {'Redemption Date':'Redemption Date', 'Redeemed Amount':'Probability'}, inplace = True)

#To find mean, we use numpy builtin function
mean = (np.array(Prob['Redemption Date'], dtype='datetime64[s]')
        .view('i8')
        .mean()
        .astype('datetime64[s]'))

mean = pd.to_datetime(mean)

#Stroring date values in temporary array
tempvar = pd.to_datetime(Prob['Redemption Date'])

#Sample Size is 5
sample = 5

std=0
x=0

#Calculating Standard Deviation
for i in range (1,5):
    std = mt.sqrt(mt.pow((tempvar[i] - mean).days,2)/(sample-1) )  
x = 0.95*(std/mt.sqrt(sample-1))

#Calculating Confidence Interval
ci_u = mean + timedelta(days=x)
ci_l = mean - timedelta(days=x)

#Printing Results

print(Prob)
print("")

print ( "Confidence Interval (95%) Lower  --->  ", ci_l.strftime("%b %d, %Y"))
print ( "Confidence Interval (95%) Upper  --->  ", ci_u.strftime("%b %d, %Y"))

print("")
print(df2)
