from func2 import *

sum_i = 0
sum_money = 0
for ind in range(CSV_COUNT):
    filename = 'dane/dane_' + str(ind) + '.csv'
    colnames=['Time','Open','High','Low','Close','Volume']
    data = pd.read_csv(filename, names=colnames, nrows=CSV_ROW_COUNT)  # import data

    calcMACD(data)
    calcSignal(data)
    calcDiff(data)


    saveGraph(data,'Close', 'Close value graph','blue', ind)
    saveGraph(data,'DIFF', 'DIFF value graph','indigo', ind)
    saveGraphMS(data,ind, False)
    saveGraphMS(data, ind, True)

    max_val = 0
    max_i = 0
    for i in range(7):
        amount, money = 0,1000
        amount,money = calcBuySellXdays(data,amount,money, i)

        if amount != 0:    #check on the last day
            money += round(amount * data['Close'].loc[data.index[CSV_ROW_COUNT - 1]], 2)
            amount = 0

        if max_val < money:
            max_val = money
            max_i = i

    print(ind, '\t', max_i, '\t', max_val)
    sum_i += max_i
    sum_money += money

print(sum_i/CSV_COUNT)
print(sum_money/CSV_COUNT)