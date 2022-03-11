# N - number of periods
# ind - index of the day for which the EMA is calculated
# data - data set from csv
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
    data['MACD'] = 0 #initialize new column
    N1 = 12 #period 1
    N2 = 26 #period 2
    for i in range(len(data)):  # len(data)
        if (i - N2) > 0:
            data.loc[i:i, 'MACD'] = calcEMA(N1, i, data, 'Open') - calcEMA(N2, i, data, 'Open')
            #print('i:', data.loc[i:i, 'MACD'])


def calcSignal(data):
    data['SIGNAL'] = 0
    for i in range(len(data)):
        data.loc[i:i, 'SIGNAL'] = calcEMA(9, i, data, 'MACD')


# tests


def test(N, ind):
    for i in range(ind, ind - N, -1):
        if (ind - i) >= 0:
            print(i)


def test2(N, ind):
    if (ind - N) < 0:
        return 0

    for i in range(ind, ind - N, -1):
        print(i)
