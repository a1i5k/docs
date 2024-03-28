import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

count_repeat = 100
N = 100
np.random.seed(0)

SCHEMA = {
    "0": {"1": 1},
    "1": {"2": 1},
    "2": {"3": 0.6, "4": 0.4},
    "3": {"0": 1},
    "4": {"0": 1},
}

array_size = len(SCHEMA)


def rand(values: dict):
    temp_value = []
    sum_digit = 0
    for key in values.keys():
        sum_digit += values[key]
        temp_value.append({sum_digit: key})

    digit = random.random()

    for value in temp_value:
        key = 0
        for k in value.keys():
            key = k
        if digit < key:
            return value[key]
    print("Не выбрано значение")
    return None


class State:
    def __init__(self, name, path):
        self.name = name
        self.next = path

    def select_next(self, all_states):
        next_name_state = rand(self.next)
        if next_name_state is None:
            return None
        for state in all_states:
            if state.name == next_name_state:
                return state
        return None


def main():
    all_state = []
    for key in SCHEMA.keys():
        all_state.append(State(name=key, path=SCHEMA[key]))

    stat = []

    step = 0
    while step < count_repeat:
        step += 1
        current_state = all_state[0]

        history_state = []
        i = 0
        while i < N:
            history_state.append(int(current_state.name))
            # Next stap
            next_state = current_state.select_next(all_state)
            if next_state is None:
                return None
            i += 1
            current_state = next_state
        stat.append(history_state)

    # Вероятность оказатсья в состоянии
    for i in range(array_size):
        count = 0
        for j in range(count_repeat):
            if stat[j][-1] == i:
                count += 1
        print(count / count_repeat)

    # Выборочные траектории частот состояний МЦ
    x = [i for i in range(N)]
    for i in range(array_size):
        y = []
        for j in range(N):
            count = 0
            for _ in range(count_repeat):
                for path in stat:
                    if path[j] == i:
                        count += 1
            y.append(count / (count_repeat * N * count_repeat / 100))
        plt.plot(x, y)

    # Отображение графиков
    plt.show()
    # Гистограмма распределения состояний МЦ
    ys = []
    for i in range(array_size):
        y = []
        for j in range(N):
            count = 0
            for _ in range(count_repeat):
                for path in stat:
                    if path[j] == i:
                        count += 1
            y.append(count / (count_repeat * N * count_repeat / 100))
        ys.append(y)
    # plt.hist(ys, bins=100, density=True, alpha=0.6, color='g')
    sns.histplot(ys, kde=True)
    # Отображение графиков
    plt.show()


if __name__ == '__main__':
    main()

