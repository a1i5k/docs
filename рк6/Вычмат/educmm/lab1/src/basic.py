import numpy
import matplotlib.pyplot as plt


def qubic_spline_coef(x_nodes, y_nodes):
    n = len(x_nodes)
    h = [x_nodes[i + 1] - x_nodes[i] for i in range(n - 1)]
    matrix_a = numpy.diag(numpy.r_[[1], [2 * (h[i + 1] + h[i]) for i in range(len(h) - 1)], [1]])
    matrix_a = matrix_a + numpy.diag(numpy.r_[[0], [h[i] for i in range(1, n - 1)]], 1)
    matrix_a = matrix_a + numpy.diag(numpy.r_[[h[i] for i in range(n - 2)], [0]], -1)

    a = numpy.array(y_nodes)

    matrix_b = numpy.r_[[0], [3 * (a[i + 2] - a[i + 1]) / h[i + 1] - 3 * (a[i + 1] - a[i]) / h[i] for i in range(n - 2)], [0]]

    c = numpy.linalg.solve(matrix_a, matrix_b)
    d = numpy.array([(c[i + 1] - c[i]) / (3 * h[i]) for i in range(n - 1)])
    b = numpy.array([(a[i + 1] - a[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3 for i in range(n - 1)])

    result = numpy.zeros((5, n - 1))
    for i in range(n - 1):
        result[0][i] = a[i]
        result[1][i] = b[i]
        result[2][i] = c[i]
        result[3][i] = d[i]
        result[4][i] = x_nodes[i]
    return result


def qubic_spline(x, qs_coeff):
    a = qs_coeff[0]
    b = qs_coeff[1]
    c = qs_coeff[2]
    d = qs_coeff[3]
    xi = qs_coeff[4]

    if x <= xi[0]:
        i = 0
        return a[i] + b[i] * (x - xi[i]) + c[i] * (x - xi[i]) ** 2 + d[i] * (x - xi[i]) ** 3

    for i in range(1, len(xi)):
        if xi[i - 1] <= x <= xi[i]:
            j = i - 1
            return a[j] + b[j] * (x - xi[j]) + c[j] * (x - xi[j]) ** 2 + d[j] * (x - xi[j]) ** 3

    if xi[-1] <= x:
        return a[-1] + b[-1] * (x - xi[-1]) + c[-1] * (x - xi[-1]) ** 2 + d[-1] * (x - xi[-1]) ** 3


def d_qubic_spline(x, qs_coeff):
    b = qs_coeff[1]
    c = qs_coeff[2]
    d = qs_coeff[3]
    xi = qs_coeff[4]

    if x < - xi[0]:
        i = 0
        return b[i] + 2 * c[i] * (x - xi[i]) + 3 * d[i] * (x - xi[i]) ** 2

    for i in range(1, len(xi)):
        if xi[i - 1] <= x <= xi[i]:
            j = i - 1
            return b[j] + 2 * c[j] * (x - xi[j]) + 3 * d[j] * (x - xi[j]) ** 2

    if xi[-1] <= x:
        i = - 1
        return b[i] + 2 * c[i] * (x - xi[i]) + 3 * d[i] * (x - xi[i]) ** 2


def graph_one():
    x = numpy.linspace(0, 1, 11)
    y = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]
    a = qubic_spline_coef(x, y)

    x1 = numpy.linspace(0, 1, 1000)
    y1 = numpy.array([qubic_spline(i, a) for i in x1])

    plt.figure(figsize=(8, 5))
    plt.xlabel('x', fontsize=14)
    plt.ylabel('h(x)', fontsize=14)
    plt.title('Кубический сплайн, проходящий через узлы из таблицы 1', fontsize=17)

    plt.plot(x1, y1)
    plt.plot(x, y, 'ro')

    plt.show()


def graph_two():
    x = numpy.linspace(0, 1, 11)
    y = [3.37, 3.95, 3.73, 3.59, 3.15, 3.15, 3.05, 3.86, 3.60, 3.70, 3.02]
    a = qubic_spline_coef(x, y)

    x1 = numpy.linspace(0, 1, 1000)
    y1 = numpy.array([d_qubic_spline(i, a) for i in x1])

    plt.figure(figsize=(8, 5))
    plt.title('Производная кубического сплайн, проходящий через узлы из таблицы 1', fontsize=14)

    plt.plot(x1, y1)
    plt.plot(x, y, 'ro')

    plt.show()


if __name__ == "__main__":
    graph_one()
    graph_two()
