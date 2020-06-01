import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt

argumenty, wartosci = [], []
f = open('dane.txt')
for line in f.readlines():
    argumenty.append(float(line[0:12]))
    wartosci.append(float(line[12:]))
f.close()


def policz_rozmiar_nowego_przedzialu(wartoscD, wartoscB, a, b, c, d):
    if (wartoscD < wartoscB):
        if (d < b):
            c = b
        elif (d > b):
            a = b
    elif (wartoscD > wartoscB):
        if (d < b):
            a = d
        elif (d > b):
            c = d
    return c - a


splajn = scipy.interpolate.CubicSpline(argumenty, wartosci, bc_type='natural')
tolerancja = 1e-5
czy_iterowac = True

# najpierw mm dwa punkty   # a...b  zakladam ze b bedzie wieksze od a
a = -0.126
b = -0.07

punkty_poczatkowe = [a, b]  # do wykresu
odleglosc = b - a
# SZUKAM TROJKI PUNKTOW WSTEPNIE OTACZAJACYCH MMINIMUM
c = 0
wartoscC = 0
znalazlem = False  # czy znalazlem trojke punktow
while (not znalazlem):
    wartoscA = splajn(a)
    wartoscB = splajn(b)
    if (wartoscA > wartoscB):  # a...b...c
        c = b + odleglosc
        wartoscC = splajn(c)
        if (wartoscC > wartoscB):  # a...b...c
            znalazlem = True
        else:  # c jest mniejsze od b, biore dwa punkty ostatnie
            a = b
            b = c
            odleglosc = 2 * odleglosc  # podwajam krok
    elif (wartoscB > wartoscA):  # c...a...b
        c = a - odleglosc
        wartoscC = splajn(c)
        if (wartoscC > wartoscA):
            znalazlem = True
            tmp = b
            b = a
            a = c
            c = tmp  # a...b...c
        else:
            b = a
            a = c
            odleglosc = 2 * odleglosc  # podwajam krok
    if (odleglosc > 10):
        print("krok wiekszy niz 10 zatem monotonicznie malejaca galaz funkcji, nic z tego nie bedzie")
        czy_iterowac = False
        break

# MAM JUZ TROJKE PUNKTOW wstepnie wyznaczajacych minimuum bedziemy iterowac metoda Brenta
wartoscA = splajn(a)
wartoscB = splajn(b)
wartoscC = splajn(c)
while (czy_iterowac):
    dlugosc_przedzialu_zawierajacego_minimum = c - a
    stareB = b  # bedzie mi potrzebne do warunku zakonczenia iteracji
    # teraz obliczam d ze wzoru (6) z wykladu
    d = 0.5 * (a * a * (wartoscC - wartoscB) + b * b * (wartoscA - wartoscC) + c * c * (wartoscB - wartoscA)) / (
            a * (wartoscC - wartoscB) + b * (wartoscA - wartoscC) + c * (wartoscB - wartoscA))
    wartoscD = splajn(d)
    # mam obliczone d i teraz moge zaakceptowac lub nie!
    akceptacjaD = False
    if (a < d and d < c):  # zeby zaakceptowac  d musi lezec miedzy a i c oraz..
        rozmiar_nowego_przedzialu = policz_rozmiar_nowego_przedzialu(wartoscD, wartoscB, a, b, c, d)
        if (
                rozmiar_nowego_przedzialu <= 0.5 * dlugosc_przedzialu_zawierajacego_minimum):  # musi jeszcze rozmiar noowego przedzialu byc mniejszy niz polowa przedzialu wczesniejszego
            akceptacjaD = True
    # jesli nie zaakceptowalem mojego d to robie bisekcje
    if (not akceptacjaD):  # rob bisekcje
        d = (a + c) / 2
        wartoscD = splajn(d)
    # mam juz ostatecznie wyznaczone d
    # licze punkt (4) z wykladu czyli wyznaczam nowy przedzial
    if (wartoscD < wartoscB):
        if (d < b):
            c = b
            b = d
            wartoscC = wartoscB
            wartoscB = wartoscD
        elif (d > b):
            a = b
            b = d
            wartoscA = wartoscB
            wartoscB = wartoscD
    elif (wartoscD > wartoscB):
        if (d < b):
            a = d
            wartoscA = wartoscD
        elif (d > b):
            c = d
            wartoscC = wartoscD
    # teraz warunek czy skonczyc iteracje poszukiwan minimum
    if (np.abs(c - a) < tolerancja * (np.abs(stareB) + np.abs(d))):
        czy_iterowac = False
print("ZNALEZIONE MINIMUM")
print(b)
print(wartoscB)
#rysuje wykres
wartosci = [splajn(punkty_poczatkowe[0]), splajn(punkty_poczatkowe[1])]
plt.plot(punkty_poczatkowe, wartosci, 'go')  # zaznaczam na wykresie punkty poczatkowe
plt.plot(b, wartoscB, 'ro')
plt.legend(['punkty poczatkowe', 'znalezione minimum'])
xplot = np.arange(-1.5, 1.5, 0.001)
plt.plot(xplot, splajn(xplot), 'b')
plt.grid(True)
plt.savefig('08zad16.png')
plt.show()