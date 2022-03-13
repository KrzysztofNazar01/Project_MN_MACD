SIZE = 1000

# N - number of periods
# ind - index of the day for which the EMA is calculated
# data - data set from csv

from matplotlib import pyplot as plt
import pandas as pd


def calcEMA(N, ind, data, colName):
    if (ind - N) < 0:
        return 0

    alfa = 1 - 2 / (N + 1)  # const
    num = 0  # numerator
    den = 0  # denominator
    for i in range(ind, ind - N, -1):
        num += data.loc[i, colName] * pow(alfa, i)
        den += pow(alfa, i)
    # print('N:', N, 'i:', ind, ' = ', (num/den))
    return (num / den)


# data - data set from csv
def calcMACD(data):
    data['MACD'] = 0  # initialize new column
    N1 = 12  # period 1
    N2 = 26  # period 2
    for i in range(SIZE):  # len(data)
        if (i - N2) > 0:
            data.loc[i:i, 'MACD'] = calcEMA(N1, i, data, 'Open') - calcEMA(N2, i, data, 'Open')
            # print('i:', data.loc[i:i, 'MACD'])


def calcSignal(data):
    data['SIGNAL'] = 0
    for i in range(SIZE):
        data.loc[i:i, 'SIGNAL'] = calcEMA(9, i, data, 'MACD')


def calcCross(data):
    data2 = data
    Y = [0, 0]  # height of the vertical line

    # set height of vertical line
    Y[0] = 1.1 * pd.DataFrame(data2, columns=['MACD']).max()
    Y[1] = 1.1 * pd.DataFrame(data2, columns=['MACD']).min()

    print(Y[0])
    print(Y[1])

    state = True
    value = 0
    for i in range(0, SIZE - 1):
        temp_value = 0
        temp_state = True
        s = data2['SIGNAL'].loc[data2.index[i]]
        m = data2['MACD'].loc[data2.index[i]]

        temp_value += m
        # print('\n\n', i, ' m: ', m, 's: ', s)

        if (s - m) > 0:
            temp_state = False

        diff_value = abs(value - temp_value)

        # there must be change of state and
        # the difference in value must be greater
        # than 15% of the maximum value in the analyzed time period
        if temp_state != state and diff_value > 0.30 * float(Y[0]):  # then draw vertical line
            X = [data2['Time'].loc[data2.index[i]], data2['Time'].loc[data2.index[i]]]
            if state == True:
                plt.plot(X, Y, color='green')
            else:
                plt.plot(X, Y, color='red')

            # save the new state and value
            value = temp_value
            state = temp_state


def calcBuySell(data, amount, money):
    state = True
    value = 0
    last_value = data['Open'].loc[data.index[0]]
    for i in range(0, SIZE - 1):
        temp_value = 0
        temp_state = True
        s = data['SIGNAL'].loc[data.index[i]]
        m = data['MACD'].loc[data.index[i]]

        temp_value += m

        if (s - m) > 0:
            temp_state = False

        diff_value = abs(value - temp_value)
        curr_val = data['Open'].loc[data.index[i]]

        # there must be change of state and
        # the difference in value must be greater
        # than 15% of the maximum value in the analyzed time period
        if temp_state != state:  # then draw vertical line
            if state == True:
                amount, money, last_value = sell(amount, money, curr_val, last_value)
            else:
                amount, money, last_value = buy(amount, money, curr_val, last_value)

            # save the new state and value
            value = temp_value
            state = temp_state

        #on the last day sell everything to maximise the amount of money(profit)
        if i == SIZE-1 and amount != 0:
            money += round(amount * curr_val, 2)
            amount = 0

    return amount, money


def buy(amount, money, val, last_value):
    if val < last_value and money != 0:
        print('BUY: for ', val)
        print('BEFORE: amount= ', amount, 'money=', money)

        amount = money / val
        money -= round(amount * val, 2)

        print('AFTER: amount= ', amount, 'money=', money, '\n')
        last_value = val
    return amount, money, last_value


def sell(amount, money, val, last_value):
    if (val > last_value and amount != 0):
        print('SELL for', val)
        print('BEFORE: amount= ', amount, 'money=', money)

        money += round(amount * val, 2)
        amount = 0

        print('AFTER: amount= ', amount, 'money=', money, '\n')
        last_value = val
    return amount, money, last_value


def calcDiff(data):
    data['DIFF'] = 0

    for i in range(0, SIZE - 1):
        s = data['SIGNAL'].loc[data.index[i]]
        m = data['MACD'].loc[data.index[i]]

        data.loc[i:i, 'DIFF'] = m - s
        # print('diff: ', m-s)
    plt.plot(data.loc[0:SIZE, 'Time'], data.loc[0:SIZE, 'DIFF'], label='DIFF', linewidth=0.3)


def showGraph():
    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel('Open')
    plt.title("MACD graph")
    plt.show()
