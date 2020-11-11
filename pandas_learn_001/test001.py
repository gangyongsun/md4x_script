import pandas as pd
import numpy as np

arr = [0, 1, 2, 3, 4]
s1 = pd.Series(arr)  # 如果不指定索引，则默认从 0 开始
print(s1)

n = np.random.randn(5)  # 创建一个随机 Ndarray 数组
# index = ['a', 'b', 'c', 'a', 'b']
# s2 = pd.Series(n, index=index)
s2 = pd.Series(n)
print(s2)
# print(s2.groupby(index).first())

d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
s3 = pd.Series(d)
# print(s3)

s1.index = ['A', 'B', 'C', 'D', 'E']
# print(s1)

s4 = s3.append(s1)
# print(s4)

s4 = s4.drop('e')
# print(s4)

s4['A'] = 6
# print(s4)
# print(s4['B'])

# print(s4[:3])
s1.index = ['a', 'b', 'c', 'd', 'e']

# print(s1)
# print(s2)

# s1 = s1.add(s2)
# s1 = s1.mul(s2)
s1 = s1.div(s2)

s1_median = s1.median()
s1_max = s1.max()
s1_sum = s1.sum()

# print(s1_median, s1_max, s1_sum)
