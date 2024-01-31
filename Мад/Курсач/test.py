import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.multivariate.factor import Factor
from statsmodels.regression.linear_model import OLS
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('csvwn.csv', encoding='latin-1', sep=';')

# print(df.head().T)

numeric = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'Y']
sns.pairplot(df[numeric])
# print(df[numeric].corr(method='spearman', numeric_only=False))

# data = np.array(df[numeric])
# f_value, p_value = stats.f_oneway(*data)
# print("F-значение:", f_value)
# print("p-значение:", p_value)
#
#
# df1 = pd.DataFrame(df[numeric])
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(df1)
# kmeans = KMeans(n_clusters=6)
# kmeans.fit(scaled_data)
# df1['Cluster'] = kmeans.labels_
# print(df1)
#
# X = df[['X1', 'X2', 'X3', 'X4', 'X5', 'X6']]
# # X = df[['X1', 'X2', 'X3', 'X4', 'X5']]
# Y = df['Y']
#
# X = sm.add_constant(X, prepend=False)
#
# model = OLS(Y, X)
# res = model.fit()
# print(res.summary())
#
# # Создание набора данных
# data = {
#     'transaction_date': df['X1'],
#     'house_price_of_unit_area': df['Y'],
#     'house_age': df['X2'],
#     'distance_to_the_nearest_MRT': df['X3'],
#     'number_of_convenience_stores': df['X4'],
#     'latitude': df['X5'],
#     'longitude': df['X6']
# }
# df2 = pd.DataFrame(data)
# X = df2[['house_age', 'distance_to_the_nearest_MRT', 'number_of_convenience_stores']]
# y = df2[['house_price_of_unit_area']]
#
# print(np.unique(y))
# y = y.astype('int')
#
# model = LinearDiscriminantAnalysis()
# model.fit(X, y)
# new_data = [[19.5, 306.5947, 9]]
# predicted_class = model.predict(new_data)
# print(f'Предсказание: {predicted_class[0]}')
#

for col in df.columns:
    df[col] = (df[col] - df[col].mean()) / df[col].std()

fa = Factor(df, n_factor=2, method='pa')
res = fa.fit()

# res.get_loadings_frame(threshold=0.3)
print(res)