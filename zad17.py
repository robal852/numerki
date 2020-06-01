import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import random


def f(x, y):  # funkcja Rosenbrocka
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2


def pochodnaX(x, y):
    return 2 * (200 * x ** 3 - 200 * x * y + x - 1)


def pochodnaY(x, y):
    return 200 * (y - x * x)


def pochodnaXX(x, y):
    return 1200 * x * x - 400 * y + 2


def pochodnaYY(x, y):
    return 200


def pochodnaXY(x, y):
    return -400 * x


def policzGradient(x, y):
    return np.transpose(np.array([pochodnaX(x, y), pochodnaY(x, y)]))


def policzHesjan(x, y, lam):
    return np.array(
        [[(1 + lam) * pochodnaXX(x, y), pochodnaXY(x, y)], [pochodnaXY(x, y), (1 + lam) * pochodnaYY(x, y)]])


# Metoda Levenberga-Marquardta
x = random.random() * 4 - 2  # punkty początkowe ustawiam tak zeby sie miescily na wykresie
y = random.random() * 4 - 2
punktyX, punktyY, punktyZ = [], [], [] # do wykresu
punktyX.append(x)
punktyY.append(y)
xi = np.transpose(np.array([x, y]))
gradient = policzGradient(xi[0], xi[1])
lam = 2.0e-9  # lambda
hesjan = policzHesjan(x, y, lam)
goto = 1
while lam > 1e-11:
    # (1)
    if (goto == 1):
        gradient = policzGradient(xi[0], xi[1])
    # (2)
    hesjan = policzHesjan(xi[0], xi[1], lam)
    xtestminusxi = np.linalg.solve(hesjan, -1 * gradient)
    xtest = xtestminusxi + xi
    if (f(xtest[0], xtest[1]) > f(xi[0], xi[1])):
        lam = lam * 8
        goto = 2
    else:
        lam = lam / 8
        xi = xtest
        goto = 1
        # zaakceptowalem xtest bo znalazlem mniejsza wartosc wiec bede zaznaczal na wykresie
        punktyX.append(xtest[0])
        punktyY.append(xtest[1])
    if lam > 1:
        print("znajdujemy sie na monotonicznej galezi funkcji, poza basenem atrakcji minimum.")
        print("no trudno")
        break

print("znalezione minimum: ", xi)

for i in range(0, len(punktyY)):
    punktyZ.append(f(punktyX[i], punktyY[i]))
X = np.linspace(-2, 2, 14)
Y = np.linspace(-2, 2, 14)
X, Y = np.meshgrid(X, Y)
Z = f(X, Y)
ax = plt.axes(projection='3d')
ax.plot_wireframe(X, Y, Z, color='grey')
xs = (punktyX)
ys = (punktyY)
zs = (punktyZ)
ax.plot(xs, ys, zs, color='red', marker='o')
ax.view_init(45, 115)
plt.savefig('wykres17v4.png')
plt.show()

# def norma(wektor):
#     return np.sqrt(np.dot(np.transpose(wektor), wektor))

# W tym momencie mozemy sie przerzucic na metode zmiennej metryki.
# x = xi[0]
# y = xi[1]
# punktyXwmetodziemetryki = []
# punktyYwmetodziemetryki = []
# punktyZwmetodziemetryki = []
# punktyXwmetodziemetryki.append(x)
# punktyYwmetodziemetryki.append(y)
# gradient = policzGradient(x, y)
# epsilon = 0.000001
# print("po levenbergu")
# print(x)
# print(y)
# while True:
#     print("siema")
#     p = np.linalg.solve(hesjan, -1 * gradient)  # p to kierunek
#     # metoda imbecyla
#     xnowe = x
#     ynowe = y
#     alfa = 0
#     while True:
#         alfa += 0.01
#         if f(x + p[0] * alfa, y + p[1] * alfa) >= f(xnowe, ynowe):
#             break
#         xnowe = x + p[0] * alfa
#         ynowe = y + p[1] * alfa
#     x = x + p[0] * alfa
#     y = y + p[1] * alfa
#     punktyXwmetodziemetryki.append(x)  # wykres
#     punktyYwmetodziemetryki.append(y)  # wykres
#     nowyGradient = policzGradient(x, y)
#     igrek = nowyGradient - gradient
#     igrektransponowany = np.transpose(igrek)
#     igrekrazyigrektranspononwany = igrek.dot(igrektransponowany)
#     p = np.transpose(p)  # zeby do wzoru z wykladu pasowalo
#     # BFGS
#     nowyHesjan = hesjan + igrekrazyigrektranspononwany / alfa * np.transpose(p).dot(igrek) - (
#         gradient.dot(np.transpose(gradient))) / (np.transpose(p).dot(hesjan).dot(p))
#     hesjan = nowyHesjan
#     gradient = nowyGradient
#     if (norma(p) < epsilon):
#         break
#
# print("wynik")
# print(x)
# print(y)
#
# for i in range(0, len(punktyY)):
#     punktyZ.append(f(punktyX[i], punktyY[i]))
# # for i in range(0, len(punktyYwmetodziemetryki)):
# #     punktyZwmetodziemetryki.append(f(punktyXwmetodziemetryki[i], punktyYwmetodziemetryki[i]))
#
# X = np.linspace(-2, 2, 16)
# Y = np.linspace(-2, 2, 16)
# X, Y = np.meshgrid(X, Y)
# Z = f(X, Y)
# ax = plt.axes(projection='3d')
# ax.plot_wireframe(X, Y, Z, color='grey')
# xs = (punktyX)
# ys = (punktyY)
# zs = (punktyZ)
# ax.plot(xs, ys, zs, color='red', marker='o')
# # xs = (punktyXwmetodziemetryki)
# # ys = (punktyYwmetodziemetryki)
# # zs = (punktyZwmetodziemetryki)
# # ax.plot(xs, ys, zs, color='blue', marker='o')
# ax.view_init(45, 115)
# # ax.scatter(1, 1, 0, color='green', marker='s')  # minimum
#
# plt.savefig('wykres17.png')
# plt.show()
