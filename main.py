from func import *


data = pd.read_csv('dane3.csv', usecols=[0, 1], delimiter=';')  # import data



calcMACD(data)
calcSignal(data)
#print(data)

plt.plot(data.loc[0:SIZE,'Time'], data.loc[0:SIZE,'MACD'])
plt.plot(data.loc[0:SIZE,'Time'], data.loc[0:SIZE,'SIGNAL'])

calcCross(data)





showGraph()