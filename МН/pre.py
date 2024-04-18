import pandas as pd
import numpy as np
from datetime import datetime


PRED_DECADE = 13
KNOW_DECADE = 7

COUNT_DECADE = 10
YEAR = 2024


def printr(l):
    i = 1
    for e in l:
        print(i, e)
        i += 1
    print()


df = pd.read_csv('weather.csv', on_bad_lines='skip', sep=';', comment='#', index_col=False)

minT = min(df['T'].values)
maxT = max(df['T'].values)
delt = (maxT - minT) / COUNT_DECADE
states = []
x = minT
while x <= maxT:
    states.append(x)
    x += delt
printr(states)

decades = range(1, PRED_DECADE + 1)
years = range(2013, YEAR + 1)
new_data = pd.DataFrame(columns=years, index=decades)
for x in years:
    for y in decades:
        new_data.loc[y, x] = []

for i in range(len(df['time'])-1):
    x = df['time'][i]
    x = datetime.strptime(x, "%d.%m.%Y %H:%M")
    temp = df['T'][i]
    decade = 0
    if x.day <= 10:
        decade = 1
    elif x.day <= 20:
        decade = 2
    else:
        decade = 3
    if ((x.month - 1) * 3 + decade) <= PRED_DECADE:
        if not np.isnan(temp):
            new_data.loc[(x.month - 1) * 3 + decade, x.year].append(temp)

# Считаем среднюю для всех декад во всех годах
means = pd.DataFrame(columns=years, index=decades)
for x in years:
    for y in decades:
        temps = new_data.loc[y, x]
        try:
            means.loc[y, x] = sum(temps) / len(temps)
        except:
            pass

# Каждую среднюю определяем в каждый диапазон
states_table = pd.DataFrame(columns=years, index=decades)
for x in years:
    for y in decades:
        state = 0
        while states[state] < means.loc[y, x]:
            state += 1
        states_table.loc[y, x] = state

# Слайд 3
# Для каждой соседней пары декад определяем во что переходит
second_matrix = pd.DataFrame(columns=range(1, COUNT_DECADE + 1), index=range(1, COUNT_DECADE + 1), dtype=np.float64)
for y in range(1, COUNT_DECADE + 1):
    for x in range(1, COUNT_DECADE + 1):
        second_matrix.loc[x, y] = 0
for y in decades:
    for x in years:
        if x != YEAR and (x != YEAR - 1):
            start = states_table.loc[y, x]
            end = states_table.loc[y, x + 1]
            second_matrix.loc[start, end] += 1

# По этим переходам определяем вероятность перехода
for y in range(1, COUNT_DECADE + 1):
    summ = sum(second_matrix.loc[y, :])
    if summ > 0:
        for x in range(1, COUNT_DECADE + 1):
            second_matrix.loc[y, x] /= summ
    else:
        second_matrix.loc[y, y] = 1

# Слайд 4
b2 = np.array([0. for x in range(1, COUNT_DECADE + 1)])
b2[states_table.loc[KNOW_DECADE, YEAR] + 1] = 1.
res = np.linalg.matrix_power(second_matrix.transpose(), PRED_DECADE - KNOW_DECADE) @ b2

printr(res)
