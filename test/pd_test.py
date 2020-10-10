import pandas as pd
import numpy as np

_time = pd.to_datetime('2019-10-10', format='%Y-%m-%d')
print(_time)
print(type(_time))

df = pd.DataFrame(np.random.randn(5, 3), index=list('abcde'), columns=['one', 'two', 'three'])
# df.ix[1, :-1] = np.nan  # 第二行，排除倒数第一个都是Nan
# df.ix[1:-1, 2] = np.nan  # 第三列，排除第一个和最后一个都是Nan

# print('\n', df.dropna())

print(df.drop(['one'], axis=1))
print(df.drop(['a', 'c'], axis=0))
