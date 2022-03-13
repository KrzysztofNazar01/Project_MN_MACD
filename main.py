from func import *

money = 1000
amount = 0

data = pd.read_csv('dane3.csv', usecols=[0, 1], delimiter=';')  # import data

calcMACD(data)
calcSignal(data)
#print(data)

#plot MACD and SIGNAL line
plt.plot(data.loc[0:SIZE,'Time'], data.loc[0:SIZE,'MACD'], label='MACD')
plt.plot(data.loc[0:SIZE,'Time'], data.loc[0:SIZE,'SIGNAL'], label='SIGNAL')

#calcDiff(data)
calcCross(data)

amount,money = calcBuySell(data,amount,money)

print('amount= ', amount, 'money=', money)

#showGraph()