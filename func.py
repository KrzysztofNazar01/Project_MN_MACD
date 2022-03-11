SIZE = 1000

# N - number of periods
# ind - index of the day for which the EMA is calculated
# data - data set from csv
import numpy
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
    for i in range(0, SIZE-1):
        temp_value = 0
        temp_state = True
        s = data2['SIGNAL'].loc[data2.index[i]]
        m = data2['MACD'].loc[data2.index[i]]

        temp_value += m
        #print('\n\n', i, ' m: ', m, 's: ', s)

        if (s - m) > 0:
            temp_state = False

        diff_value = abs(value - temp_value)

        # there must be change of state and
        # the difference in value must be greater
        # than 15% of the maximum value in the analyzed time period
        if temp_state != state and diff_value > 0.30*float(Y[0]): # then draw vertical line
            X = [data2['Time'].loc[data2.index[i]], data2['Time'].loc[data2.index[i]]]
            if state:
                plt.plot(X, Y, color='green')
            else:
                plt.plot(X, Y, color='red')

            # save the new state and value
            value = temp_value
            state = temp_state


def showGraph():
    plt.xlabel('Time')
    plt.ylabel('Open')
    plt.title("MACD graph")
    plt.show()
