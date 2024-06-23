import numpy as np
from scipy.stats import expon
import random

np.random.seed(1)
LAMBDA = 0.01
SCHEMA = {
    "0": {"1": 0.5, "2": 0.5},
    "1": {"3": 1},
    "2": {"4": 0.5, "5": 0.5},
    "3": {"6": 1},
    "4": {"6": 1},
    "5": {"6": 1},
    "6": {}
}
START = "0"
END = "6"


def rand(state, all_states):
    temp_value = []
    sum_digit = 0
    fork = []
    for key in state.next.keys():
        if state.broken is False:
            sum_digit += state.next[key]
            for i in all_states:
                if i.name == key:
                    fork.append(i)
            temp_value.append({sum_digit: key})

    if sum_digit == 0:
        return None, None

    digit = random.random()

    for value in temp_value:
        key = 0
        for k in value.keys():
            key = k
        if digit < key:
            for i in all_states:
                if i.name == value[key]:
                    fork.remove(i)
                    break
            return value[key], fork
    print("Не выбрано значение")
    return None


def convert_to_matrix(all_state):
    result = []
    for i in range(0, len(all_state)):
        row = []
        for j in range(0, len(all_state)):
            row.append(0)
        result.append(row)

    broken = []
    for i in all_state:
        if i.broken:
            broken.append(int(i.name))

    for i in all_state:
        row = []
        digit_name = []
        for j in i.next.keys():
            digit_name.append(int(j))
        # for j in range(0, len(all_state)):
        #     if j in digit_name:
        #         row.append(1)
        #     elif j == int(i.name):
        #         row.append(0)
        #     else:
        #         row.append(0)
        for j in digit_name:
            if i.broken is False and j not in broken:
                result[int(i.name)][j] = i.T
                result[j][int(i.name)] = i.T
    return result


class State:
    def __init__(self, name, path, T):
        self.name = name
        self.next = path
        self.T = T
        self.broken = False

    def select_next(self, all_states):
        next_name_state, fork = rand(self, all_states)
        if next_name_state is None:
            return None, None
        for state in all_states:
            if state.name == next_name_state:
                return state, fork
        return None


all_state = []
for key in SCHEMA.keys():
    random_sample = expon.rvs(scale=1/random.uniform(0.01, 0.02))
    all_state.append(State(name=key, path=SCHEMA[key], T=random_sample))


P = np.array(convert_to_matrix(all_state))

len_p = len(all_state)
A = np.transpose(P) - np.eye(len_p)
A[-1] = np.ones(len_p)
b = np.zeros(len_p)
b[-1] = 1

pi = np.linalg.solve(A, b)
pi_normalized = pi / np.sum(pi)

print(pi_normalized)
