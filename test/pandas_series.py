# Series：一种类似于一维数组的对象，是由一组数据(各种NumPy数据类型)以及一组与之相关的数据标签(即索引)组成。
# 仅由一组数据也可产生简单的Series对象。
# 注意：Series中的索引值是可以重复的。
import pandas as pd
import numpy as np

ser01 = pd.Series(np.array([1, 2, 3, 4]))
# print(ser01.dtype)
# print(ser01.values)
# print(ser01.index)

# 设置索引(创建好后改)
ser01.index = ['a', 'b', 'c', 'd']

ser01 = pd.Series(np.array([1, 2, 3, 4]), index=['a', 'b', 'c', 'd'])
# print(ser01)

ser02 = pd.Series({
    'a': 10,  # key变为索引
    'b': 20,
    'c': 30
})

# print(ser02)

print(ser02['a'])
print(ser02[0])
print(ser02[0:2])
print(ser02['a':'c'])
