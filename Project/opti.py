import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import yfinance as yf

#Construct your portofolio !!!
ticker_list = []
Rp=float(input(" Enter the rendement you want"))
n=int(input("Enter lenght of stocks you want to have on your portofolio"))
#Get the DATAs
for i in range (n):
    elem = input("stocks")
    ticker_list.append(elem)
    globals()[f"df{i}"]=yf.Ticker(ticker_list[i]).history(period="1y",interval="1mo")
    globals()[f"df{i}"].dropna(inplace=True)

# Calcul du rendement
def rendement_mensuel(data) :
    yolo=[0]
    for i in range (0,len(data)-1):
        yolo.append((data['Close'][i+1]-data['Close'][i])/(data['Close'][i]))
    data['rendement mensuel']= yolo
    return data 

def rendement_moyen_mensuel(data) :
    return (sum(rendement_mensuel(data)['rendement mensuel']))/(len(data)-1)

# calcul des covariances 
def cov(data1,data2) :
    E1=rendement_moyen_mensuel(data1)
    E2=rendement_moyen_mensuel(data2)
    a=0
    for i in range (0,len(data1)-1):
        a= a + (rendement_mensuel(data1)['rendement mensuel'][i] - E1)*(rendement_mensuel(data2)['rendement mensuel'][i] - E2)
    return a/(len(data1))
# Construct A^-1
a=[]

l=[0.0]*(n+2)
for i in range(n+2) :
     a.append(l)
A=np.array(a)
for i in range(n) :
    for j in range (n) :
        A[i][j]=2*cov(globals()[f"df{i}"],globals()[f"df{j}"])
        A[n][j]=rendement_moyen_mensuel(globals()[f"df{j}"])
        A[n+1][j]=1
    A[i][n]= rendement_moyen_mensuel(globals()[f"df{i}"])
    A[i][n+1] = 1
B=np.linalg.inv(A) # invert A

#Construct T
a=[]
l=[0.0]
for i in range(n+2) :
     a.append(l)
t=a  
t[n]=[Rp]
t[n+1]=[1]
T=np.array(t)

# FINISH HIM
X=np.matmul(B,T)
print(X)










   








    