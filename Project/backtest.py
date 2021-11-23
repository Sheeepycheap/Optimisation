import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import yfinance as yf
res=[]
major_indices = pd.read_html("https://www.cboe.com/us/equities/market_statistics/listed_symbols/")[0]
ticker_list= major_indices['Symbol'].to_list()
 # on met la fonction buy and sell
def buy_sell(data) :
    test1=[]
    test2=[]
    PositionSell = False # on est pas dans une position où l'on doit vendre avant de procéder à une autre action.
    for i in range (0, len(data)) :
        if data['5ema'][i]<data['20ema'][i] and data['20ema'][i]<data['60ema'][i] and  PositionSell == False :
            PositionSell = True
            test1.append(data['Close'][i])
        elif PositionSell== True and  data['5ema'][i]>data['20ema'][i] and data['20ema'][i]>data['60ema'][i] :
            test2.append(data['Close'][i])
            PositionSell= False
    return (test1,test2)
# renvoie les plus values
def pv(list1,list2) :
    if len(list1) == len(list2) :
        for i in range(0,len(list1)) :
            res.append(((list2[i] - list1[i])/list1[i])*100)
    return res 
#backtest la stratégie
def backtest( stock, period, interval):
    stock=yf.Ticker(str(stock))
    df = stock.history(period = str(period), interval=str(interval))
    df['5ema']=df['Close'].ewm(span = 5 , adjust = False).mean()
    shortEMA= df['5ema']
    df['60ema']=df['Close'].ewm(span = 60 , adjust = False).mean()
    longEMA = df['60ema']
    df['20ema']=df['Close'].ewm(span = 20 , adjust = False).mean()
    MiddleEMA=df['20ema']
    return pv(buy_sell(df)[0],buy_sell(df)[1])

#calcul les pv de tous les indices et donne une espérance des gains
for i in range(101) :
    backtest(ticker_list[i],period='1y',interval='1d')
esperance = sum(res)/(len(res))
print(esperance)

