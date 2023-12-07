import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import pandas as pd


def get_some_data():
    data = pd.read_csv('wdbc.data', delimiter=',', header=None)
    diagnosis = np.array(data)[:, 1:2].T[0]
    X = np.array(data)[:, 2:]
    result = X.astype(np.float32, copy=True)
    return result, diagnosis


def plot_data(X, diagnosis, principal_components=[]):
    fig, ax = plt.subplots(figsize=(10, 10))
    label = [1 if i == 'M' else 0 for i in diagnosis]
    colors = ['green', 'blue']

    ax.scatter(X[:, 0],
               X[:, 1],
               c=label,
               cmap=matplotlib.colors.ListedColormap(colors),
               s=18)

    max_val = np.max(np.abs(X))
    for v in principal_components:
        ax.plot([0, max_val * v[0]], [0, max_val * v[1]], linewidth=4)
    ax.set_xlabel(r'Component 1', fontsize=16)
    ax.set_ylabel(r'Component 2', fontsize=16)

    ax.plot(0, 0, 'ro', markersize=10)
    ax.grid()
    plt.show()


def normalized_data_matrix(X):
    m = X.shape[0]
    return (np.eye(m) - 1 / m * np.ones((m, m))) @ X


def pca(A):
    A = np.array(A)
    K = A.T @ A

    lambd, q = np.linalg.eig(K)

    sig = np.sqrt(lambd)
    q_sort = q[:, np.flip(np.argsort(sig))]
    return q_sort, np.flip(np.sort(np.std(A, axis=0)))


def main():
    X, diagnosis = get_some_data()
    normalized_X = normalized_data_matrix(X)
    plot_data(normalized_X, diagnosis)
    Q_T, std = pca(normalized_X)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(1 + np.arange(len(std)), std, 'o--')
    ax.set_xlabel(r'$i$', fontsize=16)
    ax.set_ylabel(r'$\sqrt{\nu} \ sigma_i$', fontsize=16)
    ax.grid()
    plt.tick_params(labelsize=16)
    plt.show()
    fig.savefig("g2.png")

    A_K = normalized_X @ Q_T[:, :2]
    plot_data(A_K, diagnosis)


if __name__ == "__main__":
    main()
