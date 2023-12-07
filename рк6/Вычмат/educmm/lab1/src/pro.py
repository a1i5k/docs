import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as st

from basic.basic_vichmat import qubic_spline, qubic_spline_coef

N = 1000
y = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]


def l_i(i, x, x_nodes):
    li = 1
    for k in range(len(x_nodes)):
        if k != i - 1:
            li = li * ((x - x_nodes[k]) / (x_nodes[i - 1] - x_nodes[k]))
    return li


def L(x, x_nodes, y_nodes):
    n = len(x_nodes)
    result = 0

    for i in range(n):
        result += y_nodes[i] * l_i(i + 1, x, x_nodes)

    return result


def task_3_a_b():
    x = np.linspace(0, 1, 11)

    rand_x = np.array([[i + np.random.normal(0, 0.01) for i in x] for _ in range(N)])
    plt.figure(figsize=(7, 5))

    for j in range(N):
        plt.plot(np.linspace(0, 1, N), [L(i, rand_x[j], y) for i in np.linspace(0, 1, N)])

    plt.plot(x, y, 'ro')
    plt.xlabel('$\ x\u0303 _i$ из таблицы 1', fontsize=14)
    plt.ylabel('$\ h _i$ из таблицы 1', fontsize=14)
    plt.title('Интерполянты Лагранжа\nсо случайной величиной и отмеченными узлами', fontsize=17)

    plt.show()


def task_3_c_d():
    x = np.linspace(0, 1, 11)

    rand_x = np.array([[i + np.random.normal(0, 0.01) for i in x] for _ in range(N)])

    Y = [[L(i, rand_x[j], y) for i in np.linspace(0, 1, N)] for j in range(N)]

    p = 0.9

    hl = np.linspace(0, 1, N)
    hu = np.linspace(0, 1, N)
    y_avg = np.linspace(0, 1, N)

    for j in range(N):
        a = [Y[i][j] for i in range(N)]
        avg = np.mean(a)
        conf_interval = st.norm.interval(p, loc=avg, scale=np.std(a))

        hl[j] = conf_interval[0]
        hu[j] = conf_interval[1]
        y_avg[j] = avg

    plt.figure(figsize=(9, 7))

    plt.plot(np.linspace(0, 1, N), hl, 'black')
    plt.plot(np.linspace(0, 1, N), hu, 'black')
    plt.plot(np.linspace(0, 1, N), y_avg, 'blue')

    plt.plot(x, y, 'ro')
    plt.xlabel('$\ x _i$ из таблицы 1\nСиний - усредненный интерполянт Лагранжа, '
               'Черный - $\ h\u0303 _i$(x) и $\ h\u0303 _u$(x)', fontsize=12)
    plt.ylabel('$\ h _i$ из таблицы 1', fontsize=14)
    plt.title('Единый график функций $\ h\u0303 _i$(x) и $\ h\u0303 _u$(x) \nусредненный интерполянт Лагранж и узлы из таблицы 1', fontsize=17)

    plt.show()


def task_4_3ab():
    x = [i / 10 for i in range(0, 11)]

    rand_y = np.array([[i + np.random.normal(0, 0.01) for i in y] for _ in range(N)])

    plt.figure(figsize=(8, 5))

    for j in range(N):
        plt.plot(np.linspace(0, 1, N), [L(i, x, rand_y[j]) for i in np.linspace(0, 1, N)])

    plt.plot(x, y, 'ro')
    plt.xlabel('$\ x _i$ из таблицы 1', fontsize=14)
    plt.ylabel('$\ h\u0303 _i$', fontsize=14)
    plt.title('Интерполянты Лагранжа со случайной величиной\n $\ h _i$ и отмеченными узлами', fontsize=17)

    plt.show()


def task_4_3cd():
    x = np.linspace(0, 1, 11)

    rand_y = np.array([[i + np.random.normal(0, 0.01) for i in y] for _ in range(N)])

    Y = [[L(i, x, rand_y[j]) for i in np.linspace(0, 1, N)] for j in range(N)]

    hl = np.linspace(0, 1, N)
    hu = np.linspace(0, 1, N)
    y_avg = np.linspace(0, 1, N)

    for j in range(N):
        a = [Y[i][j] for i in range(N)]
        mu = np.mean(a)
        conf_interval = st.norm.interval(0.9, loc=mu, scale=np.std(a))

        hl[j] = conf_interval[0]
        hu[j] = conf_interval[1]
        y_avg[j] = mu

    plt.figure(figsize=(9, 7))
    plt.plot(np.linspace(0, 1, N), hl, 'black')
    plt.plot(np.linspace(0, 1, N), hu, 'black')
    plt.plot(np.linspace(0, 1, N), y_avg, 'blue')

    plt.plot(x, y, 'ro')
    plt.title('Единый график функций $\ h\u0303 _i$(x) и $\ h\u0303 _u$(x)'
              '\nусредненный инерполянт Лагранжа и узлы из таблицы 1', fontsize=14)
    plt.xlabel('$\ x _i$ из таблицы 1\nСиний - усредненный интерполянт Лагранжа, Черный - $\ h\u0303 _i$(x) и $\ h\u0303 _u$(x) '
               'для случайной величины $\ h _i$', fontsize=10)
    plt.ylabel('$\ h _i$ из таблицы 1', fontsize=14)

    plt.show()


def task_5_3ab():
    x = [i / 10 for i in range(0, 11)]

    rand_x = np.array([[i + np.random.normal(0, 0.01) for i in x] for _ in range(N)])

    Y = [[qubic_spline(i, qubic_spline_coef(rand_x[j], y)) for i in np.linspace(0, 1, N)] for j in range(N)]

    plt.figure(figsize=(8, 5))

    for j in range(N):
        plt.plot(np.linspace(0, 1, N), Y[j])

    plt.plot(x, y, 'ro')
    plt.xlabel('$\ x\u0303 _i$ из таблицы 1', fontsize=14)
    plt.ylabel('$\ h _i$ из таблицы 1', fontsize=14)
    plt.title('Кубические сплайны со\nслучайной величиной и отмеченными узлами', fontsize=17)

    plt.show()


def task_5_3cd():
    x = np.linspace(0, 1, 11)
    rand_x = np.array([[i + np.random.normal(0, 0.01) for i in x] for _ in range(N)])
    Y = [[qubic_spline(i, qubic_spline_coef(rand_x[j], y)) for i in np.linspace(0, 1, N)] for j in range(N)]

    hl = np.linspace(0, 1, N)
    hu = np.linspace(0, 1, N)
    y_avg = np.linspace(0, 1, N)

    for j in range(N):
        a = [Y[i][j] for i in range(N)]
        mu = np.mean(a)
        conf_interval = st.norm.interval(0.9, loc=mu, scale=np.std(a))

        hl[j] = conf_interval[0]
        hu[j] = conf_interval[1]
        y_avg[j] = mu

    plt.figure(figsize=(9, 7))

    plt.plot(np.linspace(0, 1, N), hl, 'black')
    plt.plot(np.linspace(0, 1, N), hu, 'black')
    plt.plot(np.linspace(0, 1, N), y_avg, 'blue')

    plt.plot(x, y, 'ro')
    plt.xlabel('$\ x _i$ из таблицы 1\nСиний - усредненный кубический сплайн, черный -$\ h\u0303 _i$(x) и $\ h\u0303 _u$(x)', fontsize=11)
    plt.ylabel('$\ h _i$ из таблицы 1', fontsize=14)
    plt.title('Единый график функций $\ h\u0303 _i$(x) и $\ h\u0303 _u$(x)'
              '\nусредненный кубический сплайн и узлы из таблицы 1', fontsize=14)

    plt.show()


def task_5_43ab():
    x = [i / 10 for i in range(0, 11)]

    rand_y = np.array([[i + np.random.normal(0, 0.01) for i in y] for _ in range(N)])

    plt.figure(figsize=(8, 5))

    for j in range(N):
        plt.plot(np.linspace(0, 1, N),
                 [qubic_spline(i, qubic_spline_coef(x, rand_y[j])) for i in np.linspace(0, 1, N)])

    plt.xlabel('$\ x _i$ из таблицы 1', fontsize=14)
    plt.ylabel('$\ h\u0303 _i$', fontsize=14)
    plt.plot(x, y, 'ro')
    plt.title('Кубические сплайны со\nслучайной величиной $\ h _i$ и отмеченными узлами', fontsize=17)

    plt.show()


def task_5_43cd():
    x = np.linspace(0, 1, 11)

    rand_y = np.array([[i + np.random.normal(0, 0.01) for i in y] for _ in range(N)])

    Y1 = [[qubic_spline(i, qubic_spline_coef(x, rand_y[j])) for i in np.linspace(0, 1, N)] for j in range(N)]

    hl = np.linspace(0, 1, N)
    hu = np.linspace(0, 1, N)
    y_avg = np.linspace(0, 1, N)

    for j in range(N):
        a = [Y1[i][j] for i in range(N)]
        mu = np.mean(a)
        conf_interval = st.norm.interval(0.9, loc=mu, scale=np.std(a))

        hl[j] = conf_interval[0]
        hu[j] = conf_interval[1]
        y_avg[j] = mu

    plt.figure(figsize=(8, 5))
    plt.plot(np.linspace(0, 1, N), hl, 'black')
    plt.plot(np.linspace(0, 1, N), hu, 'black')
    plt.plot(np.linspace(0, 1, N), y_avg, 'blue')

    plt.xlabel('Синий - кубический сплайн Лагранжа, черный -$\ h\u0303 _i$(x) и $\ h\u0303 _u$(x) '
               'для случайно величины  $\ h _i$', fontsize=11)
    plt.ylabel('$\ h\u0303 _i$', fontsize=14)
    plt.plot(x, y, 'ro')
    plt.title('Единый график функций $\ h\u0303 _i$(x) и $\ h\u0303 _u$(x)'
              '\nусредненный кубический и узлы из таблицы 1', fontsize=16)

    plt.show()


if __name__ == "__main__":
    print('Start')
    task_3_a_b()
    print('1/8: 3_a_b done')
    task_3_c_d()
    print('2/8: 3_c_d done')
    task_4_3ab()
    print('3/8: 4_3ab done')
    task_4_3cd()
    print('4/8: 4_3cd done')
    task_5_3ab()
    print('5/8: 5_3ab done')
    task_5_3cd()
    print('6/8: 5_3cd done')
    task_5_43ab()
    print('7/8: 5_43ab done')
    task_5_43cd()
    print('8/8: 5_43cd done')
    print('Finish')
