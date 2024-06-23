import random
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

array_size = 5

SCHEMA = {}
array = np.random.rand(array_size, array_size)
for i in range(array_size):
    array[i] = array[i] / np.sum(array[i])


print(np.sum(array))
for i in range(0, array_size):
    new_value = {}
    for j in range(0, 5):
       val = array[i][j]
       new_value[str(j)] = val
    SCHEMA[str(i)] = new_value

# SCHEMA = {
#     "1": {"2": 0.5, "1": 0.5},
#     "2": {"1": 1}
# }


def rand(values: dict):
    temp_value = []
    sum_digit = 0
    for key in values.keys():
        sum_digit += values[key]
        temp_value.append({sum_digit: key})

    digit = random.random()

    # TODO: тут криво сделано, но работает
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

    current_state = all_state[0]

    history_state = [0, 0]
    i = 0
    while i < 1000:
        history_state.append(int(current_state.name))
        next_state = current_state.select_next(all_state)
        if next_state is None:
            return None
        i += 1
        current_state = next_state
        print(next_state.name)

    sns.displot(history_state, color='blue')
    plt.show()


if __name__ == '__main__':
    main()
