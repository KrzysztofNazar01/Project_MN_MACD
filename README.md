# <center> Metody Numeryczne – Projekt 1</center>
## <center>Krzysztof Nazar, 184698</center>
### <center>26 marca 2022</center>



## 1. Wstęp
Wskaźnik MACD (ang. Moving Average Convergence Divergence) to wskaźnik dynamiki trendów stworzony w latach 70-tych przez Gerald'a Appel'a. Wskaźnik MACD jest oparty na dwóch liniach: linii MACD oraz linii sygnału(SIGNAL). Linie pozwalają na analizę opłacalności sprzedaży lub kupna danej akcji

## 2. Podstawa teoretyczna
Do wyznaczania wartości wskaźnika MACD wykorzystuje się tzw. wykładniczą średnią krocząca. W celu obliczenia wartości wykładniczej kroczącej dla N okresów wykorzystuje się poniższy wzór:

$$ {EMA}_N=\frac{p_0+\left(1-\alpha\right)p_1+\ldots+\left(1-\alpha\right)^Np_N}{\left(1-\alpha\right)_.+\ldots+\left(1-\alpha\right)^N} $$

gdzie:

$ \alpha=\ \frac{2}{N-1} $ 

$ N $ – liczba okresów

$ p_i $ – wartość danej sprzed i dni


Wskaźnik MACD jest oparty na dwóch liniach. Pierwsza z nich to linia MACD wyznaczana jako różnica dwóch wykładniczych średnich kroczących(ang. EMA, Exponential Moving Average). MACD w można obliczyć za pomocą wzoru:

$$ MACD={EMA}_{12}-\ {EMA}_{26} $$

Drugą linią jest linia sygnału wyznaczana jako 9-dniowa wartość EMA obliczana z na podstawie wartości wskaźnika MACD. 

Dzięki tym dwóm liniom można ocenić czy warto kupować lub sprzedawać akcje. Jeśli linia MACD przebija od dołu linię sygnału – warto kupować. Natomiast jeśli linia MACD przebija linie sygnału od góry – warto sprzedawać. Zwykle, linie MACD oraz SIGNAL przebiegają zwykle bardzo blisko siebie, przez co często się przecinają, więc równie często generowane są odpowiednie sygnały kupna i sprzedaży. 


## 3. Zadanie projektowe
Zadanie polegało na implementacji wskaźnika MACD wraz z oceną użyteczności. Zadanie wykonałem przy użyciu języka Python. Wykorzystałem biblioteki pandas oraz matplotlib. Dane wejściowe to wektor o długości 1000 zapisany w pliku w formacie CSV. Wszystkie pliki zostały pobrane ze [strony](https://eatradingacademy.com/software/forex-historical-data/) udostępniającej historyczne dane giełdowe , a następnie zapisane w folderze „dane”. W wektorze danych zapisane są informację o cenie zamknięcia w poszczególnych dniach. Dane przedstawiają wartość akcji przez ostatnie kilka lat.

Wartość EMA obliczana jest za pomocą funkcji *CalcEMA*:


```python
def calcEMA(N, ind, data, colName):
    if (ind - N) < 0:
        return 0
    alfa = 2 / (N + 1)  # const
    num = 0  # numerator
    den = 0  # denominator
    for i in range(ind, ind - N, -1):
        num += data.loc[i, colName] * pow(1 - alfa, i)
        den += pow(1 - alfa, i)
    return (num / den)
```

Wartości wskaźnika MACD oraz linii SIGNAL dla poszczególnych dni obliczane są odpowiednio na podstawie funkcji *CalcMACD* oraz *calcSignal*:


```python
def calcMACD(data):
    data['MACD'] = 0  # initialize new column
    N1 = 12  # period 1
    N2 = 26  # period 2
    for i in range(CSV_ROW_COUNT):
        if (i - N2) > 0:
            data.loc[i:i, 'MACD'] = calcEMA(N1, i, data, 'Close') - calcEMA(N2, i, data, 'Close')
```


```python
def calcSignal(data):
    data['SIGNAL'] = 0
    for i in range(CSV_ROW_COUNT):
        data.loc[i:i, 'SIGNAL'] = calcEMA(9, i, data, 'MACD')
```

## 4. Analiza danych

Z moich obserwacji wynika, że wskaźnik MACD jest czuły na gwałtowne zmiany trendów. Jeśli następują szybkie wahania cen, widoczne jest to jako wysokie piki na wykresie przedstawiającym wartość wskaźnika. Zauważyłem, że w analizowanych wykresach raptowna zmiana wartości akcji występuje z powodu pandemii, która niekorzystnie wpłynęła na stan globalnego rynku. 

Wykresy przedstawiające linie MACD oraz SIGNAL pokazują, że obydwie linie przecinają się relatywnie często. Można przypuszczać, że wykorzystując każdą okazję na zakup lub sprzedaż akcji, przedsiębiorca wzbogacałby się często, lecz zyskiwałby relatywnie niewielkie ilości pieniędzy. 

Niestety nie ma pewności, że taki przedsiębiorca zawsze by się wzbogacał. W rzeczywistym życiu inwestowanie na giełdzie nie jest tak proste jakby mogło się wydawać. Biorąc pod uwagę tylko wskaźnik MACD, można popełnić błędy inwestycyjne. Ignorując inne narzędzia ekonomiczne można dokonać błędnej interpretacji aktualnej sytuacji na giełdzie. 

W celu upewnienia się, że sygnał kupa lub sprzedaży jest poprawny, przyjąłem, że sygnał kupna powinien zostać wygenerowany powyżej poziomu 0. Dzieje się tak, ponieważ wiadomo, że wartość EMA z poprzednich 12 dni jest większa niż z poprzednich 26 dni. Taka sytuacja wskazuje na tendencję wzrostową w wartości akcji. Zwiastuje to coraz wyższą wartość akcji w niedalekiej przyszłości. 

Co więcej, w stosowanym przeze mnie mechanizmie kupna akcji, wartość akcji musi być mniejsza niż wartość akcji, za którą ostatnio sprzedaliśmy akcje. W przypadku sprzedaży sytuacja jest odwrotna. Zakładam, że dzięki takiemu podejściu maksymalizuje się szansa na zysk.

W celu uniknięcia pochopnych decyzji podejmowanych z dnia na dzień, warto poczekać z ostateczną decyzją kupna lub sprzedaży. W celu upewnienia się, że sygnał jest poprawny można wprowadzić okres buforowy. Na przykład w przypadku sygnału kupna należy wziąć pod uwagę informacje, czy linia wskaźnika jest powyżej linii sygnału od co najmniej kilku dni – dopiero po kilku dniach wygenerowany zostanie ostateczny sygnał kupna. Analogiczny mechanizm można wprowadzić w przypadku sygnału sprzedaży. Dzięki temu przedsiębiorca jest pewny, że sytuacja jest stabilna, a szansa na zarobek staje się pewniejsza.

W programie wprowadziłem funkcje analizującą aktualny stan wartości akcji oraz mechanizm sprzedaży i kupna akcji. Na początku inwestycji użytkownik posiada kapitał w wysokości 1000 jednostek waluty oraz nie posiada żadnych akcji. Inwestowanie odbywa się automatycznie na podstawie analizy wartości wskaźnika MACD zgodnie z zasadami przedstawiony powyżej. 

Baza danych posiada 15 różnych plików csv. Każdy z nich zawiera informacje o wartości innej akcji. Pliki analizowane są pojedynczo. Dla każdego z nich tworzone są 4 wykresy przedstawiające zmiany poszczególnych wartości w analizowanym przedziale czasowym. Wykresy stworzone były za pomocą poniższych funkcji.

Funckja służąca do zapisu wykresów przedstawiających wartości akcji *Close" oraz wartości różnicy pomiędzy liniami MACD oraz SIGNAL.


```python
def saveGraph(data, ylab, tit, col, ind):
    plt.plot(pd.DatetimeIndex(data.loc[0:CSV_ROW_COUNT, 'Time']), data.loc[0:CSV_ROW_COUNT, ylab], label=ylab,
             color=col, linewidth=0.7)
    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel(ylab)

    title = tit + '_' + str(ind)
    savename = 'wykresy/' + title + '.png'

    plt.title(title)
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.savefig(savename, dpi=200)
    plt.close()
```

Funckja służąca do zapisu wykresów przedstawiających wartości linii MACD oraz SIGNAL. Zmienna *withCross* odpowiada za to, czy rysowane są wertykalne kreski informujące przecięciu się dwóch linii.


```python
def saveGraphMS(data, ind, withCross=False):
    dateTime = pd.DatetimeIndex(data.loc[0:CSV_ROW_COUNT, 'Time'])

    plt.plot(dateTime, data.loc[0:CSV_ROW_COUNT, 'MACD'], label='MACD',
             color='orange', linewidth=0.7)
    plt.plot(dateTime, data.loc[0:CSV_ROW_COUNT, 'SIGNAL'], label='SIGNAL',
             color='cyan', linewidth=0.7)
    title = 'MACD AND SIGNAL ' + str(ind)
    if withCross:
        calcCrossXDays(data, 3)
        title = 'MACD_and_SIGNAL_with_bars_' + str(ind)

    savename = 'wykresy/' + title + '.png'
    plt.title(title)
    plt.legend(loc="upper left")
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.savefig(savename, dpi=200)
    plt.close()
```

Poniżej zamieściłem przykład każdego z wykresów.


![Close value graph_4.png](attachment:41965db3-f200-412e-a20c-6a3252e195f9.png)

*<center> Obraz 1. Wykres przedstawiający zmiany wartości akcji. </center>*



![MACD AND SIGNAL 4.png](attachment:95ad5d79-1d3f-495a-9bbd-6b22cacb8971.png)

*<center> Obraz 2. Wykres przedstawiający zmiany wartości wskaźnika MACD oraz wartości SIGNAL. </center>*


![MACD_and_SIGNAL_with_bars_4.png](attachment:1f8189ac-257d-48a3-96d8-58d567e709a3.png)

*<center> Obraz 3. Wykres przedstawiający zmiany wartości wskaźnika MACD oraz wartości SIGNAL z zaznaczonymi miejscami istotnych przecięć. </center>*


![DIFF value graph_4.png](attachment:48be1b3b-2dad-4dc6-bd69-8311bfb6ccf3.png)

*<center> Obraz 4. Wykres przedstawiający zmiany wartości różnicy pomiędzy wartością wskaźnika MACD oraz wartości SIGNAL. </center>*



Przeglądając przykładowe wykresy udostępniane w Internecie, zauważyłem, że do wykresu wskaźnika MACD zwykle dołączany jest histogram przedstawiający różnicę pomiędzy aktualną wartością linii MACD oraz SIGNAL. Różnice te są przedstawione na ostatnim wykresie (Obraz 4.).

W celu wyznaczenia najlepszego okresu buforowego, stworzyłem funkcję *calcBestBufor* iterującą po wszystkich dostępnych plikach z danymi. Ta część kodu służy do wyznaczenia najlepszej długości okresu buforowego dla konkretnych danych. Maksymalna długość okresu buforowego wynosi 7 dni. Funkcja *calcBestBufor* korzysta z funkcji *calcBuySellXDays* obliczającej zysk po danym okresie czasu. Funkcja ta przyjmuje parametr *days* informujący o tym, przez ile dni linie MACD oraz SINGAL nie mogą się przecinać, żeby doszło do sprzedaży lub kupna. 


```python
def calcBuySellXdays(data, amount, money, days):
    count3Days = 0
    MACDIsUpper = True
    crossHappened = False
    if (data['SIGNAL'].loc[data.index[0]] - data['MACD'].loc[data.index[0]]) > 0:
        MACDIsUpper = False

    last_value = data['Close'].loc[data.index[0]]

    for i in range(0, CSV_ROW_COUNT - 1):
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
        if count3Days >= days and crossHappened:  # then draw vertical line
            if MACDIsUpper == True and m > 0:
                amount, money, last_value = buy(amount, money, curr_val, last_value)
            elif MACDIsUpper == False and m < 0:
                amount, money, last_value = sell(amount, money, curr_val, last_value)

            # save the new state and value
            crossHappened = False

        # on the last day sell everything to maximise the amount of money(profit)
        if i == CSV_ROW_COUNT - 1 and amount != 0:
            money += round(amount * curr_val, 2)
            amount = 0

    return amount, money
```


```python
def calcBestBufor(data):
    bestMoney = 0
    bestBufor = 0
    for i in range(7):
        amount, money = 0, 1000
        amount, money = calcBuySellXdays(data, amount, money, i)

        if amount != 0:  # check on the last day
            money += round(amount * data['Close'].loc[data.index[CSV_ROW_COUNT - 1]], 2)

        if bestMoney < money:
            bestMoney = money
            bestBufor = i

    return bestMoney, bestBufor
```

Aby końcowy wynik był bardziej wiarygodny, wyznaczam średnią arytmetyczną z wszystkich uzyskanych wyników cząstkowych.

Cała funkcja zamknięta jest w pętli iterującej po każdym dokumencie pozwalającą wyznaczyć wartości współczynnika MACD dla analizowanego zbioru danych. Wartości pobierane są z plików CSV umieszczonych w folderze „dane”, a wykresy zapisywane są w folderze „wykresy”. 



```python
from functionsMACD import *

sumBestBufor = 0
sumMoney = 0
for ind in range(CSV_COUNT):
    filename = 'dane/dane_' + str(ind) + '.csv'
    colnames=['Time','Open','High','Low','Close','Volume']
    data = pd.read_csv(filename, names=colnames, nrows=CSV_ROW_COUNT)  # import data

    calcMACD(data)
    calcSignal(data)
    calcDiff(data)

    SaveAllGraphs(data,ind)

    bestMoney, bestBufor = calcBestBufor(data)
    print(ind, '\t', bestBufor, '\t', bestMoney)
    sumBestBufor += bestBufor
    sumMoney += bestMoney

#print final average results
print(sumBestBufor/CSV_COUNT)
print(sumMoney / CSV_COUNT)
```

## 5. Wnioski

Analizując długość idealnego okresu buforowego pomiędzy 0-ma a 7-dniami, średnia najlepszej długości okresu buforowego wynosi 3,(3). A więc średnio najlepszy wynik finansowy uzyskuje się przy długości okresu między 3 a 4 dni. Szczegółowe wyniki przedstawiono w poniższej tabeli. 

|     Id pliku csv    |     Długość w dniach najlepszego okresu buforowego    |     Końcowy stan portfela    |
|:---:|:---:|:---:|
|     0     |      5       |      15768.22    |
|     1     |      2       |      762.23    |
|     2     |      6       |      1027.27    |
|     3     |      5       |      1201.45    |
|     4     |      0       |      1197.83    |
|     5     |      6       |      1225.79    |
|     6     |      3       |      4600.0    |
|     7     |      3       |      3285.57    |
|     8     |      6       |      1197.41    |
|     9     |      5       |      1205.14    |
|     10     |      3       |      1017.66    |
|     11     |      0       |      1231.01    |
|     12     |      0       |      1197.83    |
|     13     |      3       |      1181.92    |
|     14     |      3       |      1328.57    |

*<center> Tabela 1. Najbardziej opłacalna długość okresu buforowego dla analizowanych przykładów. </center>* 

Średni zysk na podstawie analizowanych danych, wynosi około 1500 jednostek waluty. Wyniki uzyskane podczas analizy dwóch pierwszych plików znacząco wyróżniają się od danych uzyskanych na podstawie innych plików. Warto zauważyć, że stosowany przeze mnie mechanizm kupna i sprzedaży nie zawsze generuje zysk finansowy. Na przykład w dokumencie o id równym 1 wartość końcowa portfela była niższa niż na początku. Wynika to z tego,  że wartość tej akcji stopniowo malała w czasie, więc trudno było na niej zarobić. Co więcej, oprócz współczynnika MACD nie brano pod uwagę innych czynników ekonomicznych, które mogły znacząco wpłynąć na wartość akcji lub poinformować o nieopłacalności inwestowania w te akcje. 

W czternastu innych przepadkach uzyskano wzrost, najwyższy(ponad 15-krotny) wzrost kapitału uzyskano dla danych zawartych w pliku o id równym 0. Wskazuje to na wysoki potencjał wykorzystywania wskaźnika MACD w praktyce. Wskaźnik z pewnością jest przydatny w analizie technicznej, a jego użytkownik może z niego wiele wywnioskować. Jednak w celu uzyskania jak najlepszych wyników finansowych, należy pamiętać o innych narzędziach do analizy aktualnej sytuacji giełdowej.

Warto zauważyć, że wraz ze wzrostem długości okresu buforowego zmniejsza się liczba generowanych sygnałów kupna oraz sprzedaży. Wynika to z faktu, że stan gdy linia MACD jest powyżej albo poniżej linii SIGNAL trwa zwykle tylko kilkanaście dni. Dla wartości np. 30 dni może wystąpić taka sytuacja, że podczas okresu 3 lat przedsiębiorca nie kupi żadnej akcji, ponieważ nie dojdzie do sytuacji, gdy linie nie będą się ze sobą przecinać przez cały miesiąc. Jest to za długi okres. Na tej podstawie uważam, że analizowany przeze mnie przedział badania najlepszej długości okresu buforowego został wybrany odpowiednio.

Wskaźnik MACD dobrze działa długofalowo. Jest wrażliwy na szybkie zmiany trendów wartości akcji. Jeśli wartość akcji w ostatnim czasie zmienia się gwałtownie, a wartości MACD mają tendencję wzrostową, można spodziewać się zmiany trendu wartości akcji. Warto zaznaczyć jeszcze raz, że w celu uzyskania jak najlepszych wyników finansowych, przedsiębiorca musi korzystać z innych źródeł informacji oraz wskaźników, aby posiadać szerszą pespektywę na panującą sytuację na giełdzie.
