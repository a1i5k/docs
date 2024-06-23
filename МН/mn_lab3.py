import random

import numpy as np

# количество един собственных значений определяет количество поглощающих состояний
# Initialize the sizes of the matrices
n = 12  # Всего
n_del = 1  # Поглощающих

# Create random matrices and normalize columns to sum to 1
MP = np.random.rand(n, n)
MP = MP / MP.sum(axis=0)
MP = MP.T

# Create a zero matrix for the combined system
SS = np.zeros((n, n))

# Place MP1 and MP2 into the combined matrix
SS[0:n, 0:n] = MP
for i in range(0, n_del):
    s = random.randint(0, n)
    SS[s, 0:n] = 0
    SS[s, s] = 1

# Calculate the eigenvalues of the combined system
for i in range(0, len(SS)):
    for j in SS[i]:
        print('%.3f' % round(j, 3), end=' ')
    print('')

print('')
e = np.linalg.eigvals(SS)
print(e)
