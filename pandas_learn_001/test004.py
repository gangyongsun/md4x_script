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

result = pd.DataFrame([s1, s2], index=['s1', 's2'])
print(result)
