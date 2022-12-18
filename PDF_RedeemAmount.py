import pandas as pd


N = 100000
W = 0.2

data = {'BMW'       : [73.69, 73.32, 50.85, 74.15, 84.69, 93.2],
        'Diageo'    : [2810 , 3114, 2842.5, 2952, 3402.5, 3878],
        'Nestle'    : [83.5 , 104.3, 104.92, 103.68, 110.44, 122.76],
        'Nike'      : [71.12 , 93.05, 92.95, 132.98, 133.27, 174.88],
        'Visa'      : [133.37 , 181.66, 193.86, 203.88, 226.44, 200.86]    
}

df = pd.DataFrame(data)

print(df)

Share_performace = []
Basket_initial = 1
Basket = []
for i in range(1, 6):
    Share_initail = df.iloc[0][i-1]
    Share_final = df.iloc[-1][i-1]
    Share_performace.append(((Share_final/Share_initail)-1)*100)
    Basket.append((Share_final/Share_initail) * W)
    
Share_min = min(Share_performace)
Share_min_index = Share_performace.index(Share_min)
WO_Share_initial = df.iloc[0][Share_min_index]
WO_Share_final = df.iloc[-1][Share_min_index]
print(f"The Worst Performing Share is : {df.columns[Share_min_index]}")
print(f"And WO Share initial is : {WO_Share_initial}")
print(f"And WO Share final is : {WO_Share_final}")
Basket_final = sum(Basket)



Date = ['27-11-2018', '27-11-2019', '27-05-2020', '27-11-2020', '27-05-2021', '26-11-2021']

Redeemed = []
Underlying_shares = ""
Redemption_Date = ""
Redeemed_Amount = 0
    
for i in range(1, 6):
    for n in range(1, 6):
        
        if df.iloc[n][i-1] >= (0.85 * df.iloc[0][i-1]):
            Underlying_shares = df.columns[i-1]
            Redemption_Date = Date[n-1]
            Redeemed_Amount = N * (1.0525 + n*0.0525)
            print(Redeemed_Amount)
        elif WO_Share_final >= (0.85 * WO_Share_initial):
            Underlying_shares = df.columns[i-1]
            Redemption_Date = Date[-1]          
            Redeemed_Amount = N * 1.315
            print(Redeemed_Amount)
        elif Basket_final > (0.85 * Basket_initial):
            Underlying_shares = df.columns[i-1]
            Redemption_Date = Date[-1]           
            Redeemed_Amount = N * 1.00
            print(Redeemed_Amount)
        else:
            Underlying_shares = df.columns[i-1]
            Redemption_Date = Date[-1]           
            Redeemed_Amount = N * ( 1.00 + (WO_Share_final - 0.85 * WO_Share_initial)/WO_Share_initial)
            print("else")
            print(Redeemed_Amount) 
        Redeemed.append({'Underlying Shares' : Underlying_shares, 'Redemption Date' : Redemption_Date, 'Redeemed Amount' : Redeemed_Amount})
ans = pd.DataFrame(Redeemed)
print(ans)
