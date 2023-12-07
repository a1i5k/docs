import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

mode = {
    'TS': [0.02, 0.2, -65, 6],
    'PS': [0.02, 0.25, -65, 6],
    'C': [0.02, 0.2, -50, 2],
    'FS': [0.1, 0.2, -65, 2],
}

I = 5
h = 0.5


def main():
    def f1(u, v):
        return 0.04 * (v ** 2) + 5 * v + 140 - u + I

    def f2(u, v):
        return a * (b * v - u)

    def euler(t0, tn, f, h):
        m = int((tn - t0) / h)

        v = np.zeros((m + 1,))
        u = np.zeros((m + 1,))

        v[0] = c
        u[0] = b * v[0]

        for i in range(m):
            v[i + 1] = v[i] + h * f[0](u[i], v[i])
            u[i + 1] = u[i] + h * f[1](u[i], v[i])

            if v[i + 1] >= 30:
                v[i + 1] = c
                u[i + 1] = u[i + 1] + d

        return u, v

    def implicit_euler(t0, tn, f, h):

        def phi_v(vi_1, ui, vi):
            return vi_1 - vi - h * f[0](u[i], v[i])

        def phi_u(ui_1, ui, vi):
            return ui_1 - ui - h * f[1](u[i], v[i])

        m = int((tn - t0) / h)

        v = np.zeros((m + 1,))
        u = np.zeros((m + 1,))

        v[0] = c
        u[0] = b * v[0]
        for i in range(m):
            v[i + 1] = optimize.fsolve(phi_v, v[i], args=(u[i], v[i]))
            u[i + 1] = optimize.fsolve(phi_u, v[i], args=(u[i], v[i]))
            if v[i + 1] >= 30:
                v[i + 1] = c
                u[i + 1] = u[i + 1] + d

        return u, v

    def runge_kutta(t0, tn, f, h):
        m = int((tn - t0) / h)

        v = np.zeros((m + 1,))
        u = np.zeros((m + 1,))

        v[0] = c
        u[0] = b * v[0]

        for i in range(m):
            vk1 = h * f[0](u[i], v[i])
            vk2 = h * f[0](u[i] + h / 2, v[i] + vk1 / 2)
            vk3 = h * f[0](u[i] + h / 2, v[i] + vk2 / 2)
            vk4 = h * f[0](u[i] + h, v[i] + vk3)

            uk1 = h * f[1](u[i], v[i])
            uk2 = h * f[1](u[i] + uk1 / 2, v[i] + h / 2)
            uk3 = h * f[1](u[i] + uk2 / 2, v[i] + h / 2)
            uk4 = h * f[1](u[i] + uk3, v[i] + h)

            v[i + 1] = v[i] + (vk1 + 2 * vk2 + 2 * vk3 + vk4) / 6
            u[i + 1] = u[i] + (uk1 + 2 * uk2 + 2 * uk3 + uk4) / 6
            if v[i + 1] >= 30:
                v[i + 1] = c
                u[i + 1] = u[i + 1] + d

        return u, v

    t0 = 0
    tn = 100

    t = np.linspace(t0, tn, int((tn - t0) / h) + 1)

    fig, axs = plt.subplots(4, 1, figsize=(14, 20))
    names = ['Tonic spiking', 'Phasic spiking', 'Chattering', 'Fast spiking']

    for i, j, ax in zip(['TS', 'PS', 'C', 'FS'], names, axs):
        a = mode[i][0]
        b = mode[i][1]
        c = mode[i][2]
        d = mode[i][3]

        u_euler, v_euler = euler(t0, tn, [f1, f2], h)
        u_implicit_euler, v_implicit_euler = implicit_euler(t0, tn, [f1, f2], h)
        u_runge_kutta, v_runge_kutta = runge_kutta(t0, tn, [f1, f2], h)

        ax.set_title(j)
        ax.plot(t, v_euler, 's--', label='Метод Эйлера', markersize=10)
        ax.plot(t, v_implicit_euler, 'o--', label='Неявный метод Эйлера', markersize=5)
        ax.plot(t, v_runge_kutta, 'o--', label='Метод Рунге-Кута', markersize=5)

        ax.grid()
        ax.legend()

    plt.show()
    fig.savefig("result.png")


if __name__ == '__main__':
    main()
