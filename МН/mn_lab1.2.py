from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

K = 11        # размерность цепи
p = 0.5
q = 1 - p     # вероятности переходов в соседние состояния (победы)
X0 = 10        # начальное состояние (начальный капитал)
N = 100     # количество повторных реализаций


def f(k, x0):
    # Цикл повторных разыгрываний цепи
    N1 = 0
    NK = 0  # Обнуление результатов статистики
    for n in range(N):
        x = x0
        while x != 1 and x != k:
            if np.random.rand() > q:
                x = x + 1
            else:
                x = x - 1
        if x == 1:
            N1 += 1
        else:
            NK += 1

    return N1 / N  # результат - вероятность разорения


# Значения X и Y
range_x = []
range_y = []
range_p = []
for k in range(4, K):
    for x0 in range(2, k-1):
        range_x.append(k)
        range_y.append(x0)
        range_p.append(f(k, x0))

# Построение 3D-графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(range_x, range_y, range_p)
# Отображение графика
plt.show()
