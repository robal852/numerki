import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize


def wielomian(x, *args):
    return (np.polyval(args, x))


argumenty, wartosci = [], []
f = open('dane20')
for line in f.readlines():
    argumenty.append(float(line[0:9]))
    wartosci.append(float(line[9:]))
f.close()

akaike = []  # tu trzymam wartosci AIC dla kolejnych wielomianow o coraz wiekszych stopniach (od 2 do 18 parametrow czyli stopien 1 do 17)

for liczbaParametrow in range(2, 19):
    poczatkowy = np.zeros(liczbaParametrow)
    params, params_covariance = scipy.optimize.curve_fit(xdata=argumenty, ydata=wartosci, f=wielomian, p0=poczatkowy,
                                                         method='lm')
    suma = 0
    for x in range(len(argumenty)):
        suma += (wartosci[x] - wielomian(argumenty[x], *params)) ** 2
    sigmaKwadrat = (suma) / len(argumenty)  # błąd (ale nie ze zle zrobione)

    AIC = np.log(sigmaKwadrat) + 2 * liczbaParametrow / len(argumenty)
    akaike.append(AIC)

print(akaike)  # najmniejsza wartosc w 2. wiec dla 3 wspolczynnikow czyli funkcji kwadratowej
xplot = []
for i in range(1, 18):
    xplot.append(i)
plt.plot(xplot, akaike, 'ro')
plt.grid(True)
plt.ylabel('wartość AIC')
plt.xlabel('stopień wielomianu')
plt.show()

poczatkowy = np.zeros(3)
params, params_covariance = scipy.optimize.curve_fit(xdata=argumenty, ydata=wartosci, f=wielomian, p0=poczatkowy,
                                                     method='lm')
print(params_covariance)  # params covariance to macierz kowarjancji estymatorow

xplot, yplot = [], []
for x in np.arange(-1, 1, 0.01):
    pomocnicza = list(params)
    pomocnicza.insert(0, x)
    y = wielomian(*pomocnicza)
    xplot.append(x)
    yplot.append(y)
plt.plot(xplot, yplot, 'blue')
plt.plot(argumenty, wartosci, 'ro')
plt.grid(True)
plt.legend(['wielomian drugiego stopnia', 'punkty danych'])
plt.show()

# ******************************************************
# do wykresu z wielomianami

# if liczbaParametrow==2:
#     kolor='green'
# elif liczbaParametrow==3:
#     kolor='blue'
# elif liczbaParametrow==4:
#     kolor='yellow'
# elif liczbaParametrow==5:
#     kolor='cyan'
# xplot, yplot = [], []
# for x in np.arange(-1, 1, 0.01):
#     pomocnicza = list(params)
#     pomocnicza.insert(0, x)
#     y = wielomian(*pomocnicza)
#     xplot.append(x)
#     yplot.append(y)
# plt.plot(xplot, yplot, kolor)

# plt.plot(argumenty, wartosci, 'ro')
# plt.grid(True)
# plt.legend(['wielomian pierwszego stopnia', 'wielomian drugiego stopnia', 'wielomian trzeciego stopnia',
#             'wielomian czwartego stopnia', 'punkty danych'])
# plt.show()
# ******************************************************