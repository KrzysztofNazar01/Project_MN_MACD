import pandas as pd
import matplotlib.pyplot as plt


from func import *


data = pd.read_csv('dane3.csv', usecols=[0, 1], delimiter=';')  # import data


calcMACD(data)
calcSignal(data)
print(data)

plt.plot(data['Time'], data['MACD'])
plt.plot(data['Time'], data['SIGNAL'])

plt.xlabel('Time')
plt.ylabel('Open')
plt.title("MACD graph")
plt.show()