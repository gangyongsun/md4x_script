import pandas as pd

df = pd.DataFrame([
    ['green', 'M', 10.1, 'class1'],
    ['red', 'L', 13.5, 'class2'],
    ['blue', 'XL', 15.3, 'class1']])
# print(df)
# print(df.loc[1])
# print(df.loc[0:1])
# print(df.iloc[0:1])
# print(df.loc[:, 0:1])


data = [[1, 2, 3], [4, 5, 6]]
index = [0, 1]
columns = ['a', 'b', 'c']
df = pd.DataFrame(data=data, index=index, columns=columns)

# print(df.loc[1])

index = ['d', 'e']
df = pd.DataFrame(data=data, index=index, columns=columns)
print(df)
print(df.loc['d'])
print(df.loc['d'].sum())
# print(df.loc['d':])
# print(df.loc['d', ['b', 'c']])
# print(df.loc[:, ['c']])
