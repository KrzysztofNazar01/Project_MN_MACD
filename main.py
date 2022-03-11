import pandas as pd

import csv

def ema(N, p):
    alfa = 1- 2/(N+1)

    for i in range(p):
        print(p)


data = pd.read_csv('dane2.csv') #import data

#print (data.loc[2:6,['open']])
#print(csvFile) #print data





