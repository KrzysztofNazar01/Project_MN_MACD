#import librarys
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
#set number of rows analyzed from csv file
SIZE = 1000


# N - number of periods
# ind - index of the day for which the EMA is calculated
# data - data set from csv
def calcEMA(N, ind, data, colName):
    if (ind - N) < 0:
        return 0

    alfa = 2 / (N + 1)  # const
    num = 0  # numerator
    den = 0  # denominator
    for i in range(ind, ind - N, -1):
        num += data.loc[i, colName] * pow(1-alfa, i)
        den += pow(1-alfa, i)
    return (num / den)


# data - data set from csv
def calcMACD(data):
    data['MACD'] = 0  # initialize new column
    N1 = 12  # period 1
    N2 = 26  # period 2
    for i in range(SIZE):
        if (i - N2) > 0:
            data.loc[i:i, 'MACD'] = calcEMA(N1, i, data, 'Close') - calcEMA(N2, i, data, 'Close')

# data - data set from csv
def calcSignal(data):
    data['SIGNAL'] = 0
    for i in range(SIZE):
        data.loc[i:i, 'SIGNAL'] = calcEMA(9, i, data, 'MACD')

# data - data set from csv
# days - for how many days MACD line must be below or under SIGNAL line to generate buy or sell signal
def calcCrossXDays(data, days):

    Y = [0, 0]  # height of the vertical line

    # set height of vertical line
    Y[0] = 1.1 * pd.DataFrame(data, columns=['MACD']).max()
    Y[1] = 1.1 * pd.DataFrame(data, columns=['MACD']).min()

    countXDays = 0
    MACDIsUpper = True
    crossHappened = False

    if (data['SIGNAL'].loc[data.index[0]] - data['MACD'].loc[data.index[0]]) > 0:
        MACDIsUpper = False

    for i in range(0, SIZE - 1):
        temp_MACDIsUpper = True
        s = data['SIGNAL'].loc[data.index[i]]
        m = data['MACD'].loc[data.index[i]]

        if (s - m) > 0:
            temp_MACDIsUpper = False

        if temp_MACDIsUpper != MACDIsUpper:
            MACDIsUpper = temp_MACDIsUpper
            countXDays = 0  # Cross happened, so zero the days counter
            crossHappened = True

        if crossHappened:
            countXDays += 1

        if countXDays >= days and crossHappened:  # then draw vertical line
            X = [data['Time'].loc[data.index[i]], data['Time'].loc[data.index[i]]]
            if MACDIsUpper == True:
                plt.plot(X, Y, color='green')  # buy
            else:
                plt.plot(X, Y, color='red')  # sell
            crossHappened = False


#data - data from csv file
#amount - current number of possesed actions
#money - current value of possesed money
# days - for how many days MACD line must be below or under SIGNAL line to buy or sell actions
def calcBuySellXdays(data, amount, money, days):
    count3Days = 0
    MACDIsUpper = True
    crossHappened = False
    if (data['SIGNAL'].loc[data.index[0]] - data['MACD'].loc[data.index[0]]) > 0:
        MACDIsUpper = False

    last_value = data['Close'].loc[data.index[0]]

    for i in range(0, SIZE - 1):
        temp_value = 0
        s = data['SIGNAL'].loc[data.index[i]]
        m = data['MACD'].loc[data.index[i]]

        temp_value += m
        curr_val = data['Close'].loc[data.index[i]]

        temp_MACDIsUpper = True
        if (s - m) > 0:
            temp_MACDIsUpper = False
        if temp_MACDIsUpper != MACDIsUpper:
            MACDIsUpper = temp_MACDIsUpper
            count3Days = 0  # Cross happened, so zero the days counter
            crossHappened = True
        if crossHappened:
            count3Days += 1

        # there must be change of state
        if count3Days >= days and crossHappened:# then draw vertical line
            if MACDIsUpper:
                amount, money, last_value = buy(amount, money, curr_val, last_value)
            else:
                amount, money, last_value = sell(amount, money, curr_val, last_value)

            # save the new state and value
            crossHappened = False

        # on the last day sell everything to maximise the amount of money(profit)
        if i == SIZE - 1 and amount != 0:
            money += round(amount * curr_val, 2)
            amount = 0

    return amount, money

def buy(amount, money, val, last_value):
    if val < last_value and money != 0:
        amount += money / val
        money -= round(amount * val, 2)
        last_value = val
    return amount, money, last_value


def sell(amount, money, val, last_value):
    if (val > last_value and amount != 0):
        money += round(amount * val, 2)
        amount = 0

        #print('AFTER: amount= ', amount, 'money=', money, '\n')
        last_value = val
    return amount, money, last_value


def calcDiff(data):
    data['DIFF'] = 0

    for i in range(0, SIZE - 1):
        s = data['SIGNAL'].loc[data.index[i]]
        m = data['MACD'].loc[data.index[i]]
        data.loc[i:i, 'DIFF'] = m - s



def saveGraph(data, ylab, tit, col, ind):
    plt.plot(data.loc[0:SIZE, 'Time'], data.loc[0:SIZE, ylab], label=ylab, color=col)
    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel(ylab)

    title =  tit + '_' + str(ind)
    savename = 'saved/' + title + '.png'

    plt.title(title)
    plt.savefig(savename, dpi=200)
    plt.close()

def saveGraphMS(data, ind, withCross = False):
    plt.plot(data.loc[0:SIZE, 'Time'], data.loc[0:SIZE, 'MACD'], label='MACD', color='orange')
    plt.plot(data.loc[0:SIZE, 'Time'], data.loc[0:SIZE, 'SIGNAL'], label='SIGNAL', color='black')
    title = 'MACD AND SIGNAL '+ str(ind)

    if withCross:
        calcCrossXDays(data,3)
        title = 'MACD_and_SIGNAL_with_bars ' + str(ind)

    savename = 'saved/' + title + '.png'
    plt.title(title)
    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.savefig(savename, dpi=200)
    plt.close()