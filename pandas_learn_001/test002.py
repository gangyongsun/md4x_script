import pandas as pd
import numpy as np

dates = pd.date_range('today', periods=6)  # 定义时间序列作为 index
num_arr = np.random.randn(6, 4)  # 传入 numpy 随机数组
columns = ['A', 'B', 'C', 'D']  # 将列表作为列名

df1 = pd.DataFrame(num_arr, index=dates, columns=columns)
print(df1)

data = {'animal': ['cat', 'cat', 'snake', 'dog', 'dog', 'cat', 'snake', 'cat', 'dog', 'dog'],
        'age': [2.5, 3, 0.5, np.nan, 5, 2, 4.5, np.nan, 7, 3],
        'visits': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        'priority': ['yes', 'yes', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no']}

labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
df2 = pd.DataFrame(data, index=labels)
# print(df2)
# print(df2.T)
# print(df2.head())
# print(df2.tail(3))
# print(df2.columns)
# print(df2.values)
# print(df2.index)
# print(df2.describe())

# print(df2['age'])
# print(df2.iloc[1:3])
# print(df2.iat[2,0])
# print(df2.loc['f','age'])

num = pd.Series([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], index=df2.index)
df2['No.'] = num  # 添加以 'No.' 为列名的新数据列

# print(df2)

# df2 = df2.drop('No.', axis=1).drop(['a','c']).dropna()
# print(df2)

# df2 = df2.fillna(value=3)
# print(df2)

# print(df2[df2['age'] > 3])
# print(df2[(df2['animal'] == 'cat') & (df2['age'] < 3)])

# print(df2[df2['animal'].isin(['cat', 'dog'])])

# print(df2.iloc[2:4, 1:3])

df2 = df2.sort_values(by=['age', 'visits'], ascending=[False, True])
# print(df2)

temp_df = df2.groupby(['animal', 'age'])['visits'].count()
# print(temp_df)
temp_df = pd.DataFrame(temp_df)
temp_df.columns = ['count']
print(temp_df)
# print(df2['animal'].unique())


df2['priority'] = df2['priority'].map({'yes': True, 'no': False})
# print(df2)

# print(df2.groupby('animal').sum())
# print(df2.groupby('animal').mean())

# df2.to_csv('./animal.csv')

df_animal = pd.read_csv('./animal.csv')
# print(df_animal)

# df2.to_excel('./animal.xlsx', sheet_name='animal')

df_excel = pd.read_excel('./animal.xlsx', 'animal', index_col=None, na_values=['NA'])
# print(df_excel.reset_index(drop=True))

# print(df_excel.median())
# print(df_excel.max())
# print(df_excel.min())
