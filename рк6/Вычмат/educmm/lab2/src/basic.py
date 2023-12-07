import numpy
import matplotlib.pyplot as plt
import numpy as np

C = 1.03439984
T = 1.75418438


def qubic_spline_coef(x_nodes, y_nodes, n):
    h = [x_nodes[i + 1] - x_nodes[i] for i in range(n - 1)]
    matrix_a = numpy.diag(numpy.r_[[1], [2 * (h[i + 1] + h[i]) for i in range(len(h) - 1)], [1]])
    matrix_a = matrix_a + numpy.diag(numpy.r_[[0], [h[i] for i in range(1, n - 1)]], 1)
    matrix_a = matrix_a + numpy.diag(numpy.r_[[h[i] for i in range(n - 2)], [0]], -1)

    a = numpy.array(y_nodes)

    matrix_b = numpy.r_[[0], [3 * (a[i + 2] - a[i + 1]) / h[i + 1] - 3 * (a[i + 1] - a[i]) / h[i] for i in range(n - 2)], [0]]

    c = numpy.linalg.solve(matrix_a, matrix_b)
    d = numpy.array([(c[i + 1] - c[i]) / (3 * h[i]) for i in range(n - 1)])
    b = numpy.array([(a[i + 1] - a[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3 for i in range(n - 1)])

    qs_coeff = np.concatenate([a, b, c, d])
    return qs_coeff


def binary_search(arr, x):
    first = 0
    last = len(arr) - 1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first + last) // 2
        if arr[mid] == x:
            index = mid
        else:
            if arr[mid] > x:
                last = mid
            else:
                first = mid
        if x <= arr[0]:
            index = 0
        if x >= (arr[len(arr) - 2]):
            index = len(arr) - 2
        if first + 1 == last:
            index = first
    return index


def qubic_spline(x, x_nodes, qs_coeff, n):
    index = binary_search(x_nodes, x)
    s = qs_coeff[index] + qs_coeff[index + n] * (x - x_nodes[index]) + qs_coeff[index + 2 * n - 1] * (
                x - x_nodes[index]) ** 2 + \
        qs_coeff[index + 3 * n - 1] * (x - x_nodes[index]) ** 3
    return s


def d_qubic_spline(x, x_nodes, qs_coeff, n):
    index = binary_search(x_nodes, x)
    d_s = qs_coeff[index + n] + 2 * qs_coeff[index + 2 * n - 1] * (x - x_nodes[index]) + 3 * qs_coeff[
        index + 3 * n - 1] * (x - x_nodes[index]) ** 2
    return d_s


def composite_simpson(a, b, n, f):
    if n % 2 == 0:
        n += 1
    segments = n - 1
    h = (b - a) / segments
    simpson = (h / 3) * (f(a) + f(b))
    for i in range(1, int((segments / 2))):
        simpson += (h / 3) * 2 * (f(a + (2 * i) * h))
    for i in range(1, int(segments / 2 + 1)):
        simpson += (h / 3) * 4 * (f(a + (2 * i - 1) * h))
    return simpson


def composite_trapezoid(a, b, n, f):
    segments = n - 1
    h = (b - a) / segments
    trapezoid = (h / 2) * (f(a) + f(b))
    for i in range(2, segments + 1):
        trapezoid += (h / 2) * 2 * (f(a + (i - 1) * h))
    return trapezoid


if __name__ == "__main__":
    n_s = 10000
    c_t = np.linspace(0, T, n_s)
    x_t = [C * (t - (1 / 2) * np.sin(2 * t)) for t in c_t]
    y_t = [C * ((1 / 2) - (1 / 2) * np.cos(2 * t)) for t in c_t]
    qs_coeff = qubic_spline_coef(x_t, y_t, n_s)


    def f(x_i):
        g = 9.8
        y = qubic_spline(x_i, x_t, qs_coeff, n_s)
        d_y = d_qubic_spline(x_i, x_t, qs_coeff, n_s)
        return np.sqrt((1 + (d_y ** 2)) / (2 * g * y))


    a = 0.01
    b = 2
    int_simp = [0] * 5000
    int_trap = [0] * 5000
    h_integral = [0] * 5000
    i = 0
    true_integral = composite_simpson(a, b, 20000, f)
    for n in range(3, 10000, 2):
        h_integral[i] = (b - a) / (n - 1)
        int_simp[i] = abs(true_integral - composite_simpson(a, b, n, f))
        int_trap[i] = abs(true_integral - composite_trapezoid(a, b, n, f))
        i += 1

    fig, ax = plt.subplots()
    plt.loglog(h_integral, int_simp, 'o', label='Simpson')
    plt.loglog(h_integral, int_trap, 'o', label='Trapezoid')
    h_for_line = np.logspace(-3, -2, 100)
    ax.loglog(h_for_line, 50 * h_for_line ** 2, 'k-', label=r'$O(h^2)$')
    ax.loglog(h_for_line, 10000 * h_for_line ** 4, 'k--', label=r'$O(h^4)$')
    plt.legend()
    plt.grid()
    plt.show()
