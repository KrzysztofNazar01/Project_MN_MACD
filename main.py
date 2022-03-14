from func2 import *

for ind in range(9):
    filename = 'dane/dane_' + str(ind) + '.csv'
    colnames=['Time','Open','High','Low','Close','Volume']
    data = pd.read_csv(filename,  names=colnames,  nrows=SIZE)  # import data

    calcMACD(data)
    calcSignal(data)
    calcDiff(data)


    #saveGraph(data,'Close', 'Close value graph','blue', ind)
    #saveGraphMS(data, ind, True)
    #saveGraphMS(data,ind, False)
    #saveGraph(data,'DIFF', 'DIFF value graph','indigo', ind)

    max_val = 0
    max_i = 0
    for i in range(30):
        amount, money = 0,100
        amount,money = calcBuySellXdays(data,amount,money, i)

        if amount != 0:    #check last day
            #print('LAST DAY SELLING')
            money += round(amount * data['Close'].loc[data.index[SIZE-1]], 2)
            amount = 0

        if max_val < money:
            max_val = money
            max_i = i

    print('i:',max_i, '\tmoney=', max_val)
