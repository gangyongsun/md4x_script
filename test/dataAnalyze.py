import matplotlib.pyplot as plt

dog_arr = plt.imread('./dog.png')

print(dog_arr)
# plt.imshow(dog_arr)
# plt.imshow(dog_arr[::-1])
# plt.imshow(dog_arr[:,::-1,:])
# plt.imshow(dog_arr[:,:,::-1])
plt.show()

import numpy as np

'''
zeros()返回一个全0的n维数组，一共有三个参数：shape（用来指定返回数组的大小）、dtype（数组元素的类型）、order（是否以内存中的C或Fortran连续（行或列）顺序存储多维数据）。
后两个参数都是可选的，一般只需设定第一个参数。
'''
zero_array = np.zeros(5)
zero_array = np.zeros((5,), dtype=np.int)
zero_array = np.zeros((2, 3))
# print(zero_array)


'''
ones()返回一个全1的n维数组，同样也有三个参数：shape（用来指定返回数组的大小）、dtype（数组元素的类型）、order（是否以内存中的C或Fortran连续（行或列）顺序存储多维数据）。
后两个参数都是可选的，一般只需设定第一个参数。和zeros一样
'''
one_array = np.ones(5)
one_array = np.ones((5,), dtype=np.int)
one_array = np.ones((2, 3))
# print(one_array)


'''
生成指定范围内指定个数的一维数组
linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None):

- 在指定的间隔[“start”,“stop”]内均匀地返回数字。
- “num”返回num个等间距的样本。
- endpoint是一个bool类型的值，如果为"Ture",“stop"是最后一个值，如果为"False”,生成的数组不会包含"stop"值
- retstep是一个bool类型的值，如果为"Ture"，会返回样本之间的间隙。
  其他相似的函数 
-  arange 和 linespace 相似，但是使用步长而不是样本的数量来确定生成样本的数量。
'''
space_array = np.linspace(3, 20, 11, endpoint=True, retstep=True, dtype=np.int)
# print(space_array)

'''
返回一个有终点和起点的固定步长的排列
1）一个参数时，终点，起点默认值0，步长默认值1。
2）两个参数时，起点，终点，步长默认值1。
3）三个参数时，起点，终点，步长。其中步长支持小数
'''
arrange_array = np.arange(5)
# print(arrange_array)

arrange_array = np.arange(5, 8)
# print(arrange_array)

arrange_array = np.arange(5, 15, 3)
# print(arrange_array)

'''
作用：生成指定区间[low, high)的随机整数
参数：
-- low: 最小值，int型
-- high: 最大值，int型
-- size: 数组维度，int型或由int构成的tuple型
-- dtype: 数据类型，默认为np.int
返回：int型或者由int构成的ndarray
'''

random_data = np.random.randint(4)  # 只有一个参数，默认生成一个[0, 4)的随机整数
# print(random_data)

random_data = np.random.randint(1, 4)  # 两个参数，生成一个在[1, 4)的随机整数
# print(random_data)

random_data = np.random.randint(4, size=3)  # 生成3个[0, 4)的随机整数
# print(random_data)

random_data = np.random.randint(-2, 5, size=(2, 4))  # 在[-2,5]区间上，生成shape为2*4的随机整数
# print(random_data)

'''
作用：生成[0, 1)之间的指定形状的随机浮点数
参数：d0, d1, ..., dn，int类型，如不写则返回单个随机数
返回：ndarray类型，形状（d0, d1, ..., dn）
'''

rand_data = np.random.rand()  # 没有参数则直接生成一个[0,1)区间的随机数
# print(rand_data)

rand_data = np.random.rand(3)  # 只有一个参数则生成n*1个随机数
# print(rand_data)

rand_data = np.random.rand(2, 3, 4)  # 有多个参数，则生成对应形状随机数，如本例生成shape为2*3*4的随机数
# print(rand_data)


'''
作用：生成指定形状,服从标准正态分布（均值为0，标准差为1）的随机数
参数：d0, d1, ..., dn，int型，如不写则返回单个标准正态分布实例
返回：ndarray类型，形状（d0, d1, ..., dn）
'''
randn_data = np.random.randn()  # 没有参数则直接随机生成一个标准正态分布实例
# print(randn_data)

randn_data = np.random.randn(3)  # 只有一个参数则生成n*1的服从标准正态分布的随机数
# print(randn_data)

randn_data = np.random.randn(2, 3, 4)  # 有多个参数，则生成对应形状标准正态分布随机数，如本例生成shape为2*3*4的服从标准正态分布的随机数
# print(randn_data)

'''
作用：从给定的一维数组中生成随机数
参数：
-- a: 一维数组或int型
-- size: 数组维度，int型或由int构成的tuple型
-- replace: 布尔型，False时生成的随机数无重复
-- p: 为a的数据设置概率，不设置时默认为均匀分布
返回：单个样本或多个样本构成的ndarray类型
'''
random_data = np.random.random()  # 没有参数，直接生成一个[0, 1)区间随机浮点数
# print(random_data)

random_data = np.random.random(3)  # 一个参数，生成[0, 1)区间shape为3*1的随机浮点数
# print(random_data)

random_data = np.random.random(size=(3, 4))  # tuple型参数，生成[0, 1)区间shape为3*4的随机浮点数
# print(random_data)

'''
作用：从给定的一维数组中生成随机数
参数：
-- a: 一维数组或int型
-- size: 数组维度，int型或由int构成的tuple型
-- replace: 布尔型，False时生成的随机数无重复
-- p: 为a的数据设置概率，不设置时默认为均匀分布
返回：单个样本或多个样本构成的ndarray类型
'''

np_random_data = np.random.choice([1, 3, 5, 7])  # 只有一个参数a,从a中随机选一个
# print(np_random_data)

np_random_data = np.random.choice([1, 3, 5, 7], size=2)  # 指定size，从a中随机选2个
# print(np_random_data)

np_random_data = np.random.choice([1, 3, 5, 7], size=(2, 3))  # size为tuple，从a中随机选2*3个
# print(np_random_data)

np_random_data = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9], size=(2, 3), replace=False)  # replace设置为false时，生成的随机数不重复
# print(np_random_data)

np_random_data = np.random.choice([1, 2, 3, 4], size=2, p=(0.1, 0.2, 0.3, 0.4))  # 设置p，根据p的权重随机挑选
# print(np_random_data)

'''
常用属性
shape #返回数组的形状:几行几列
ndim #返回数组的维度
size #返回数组元素中总共有多少个元素
dtype #返回的是数组元素的数据类型
'''
a = np.arange(15).reshape(3, 5)

# print(a.shape)

# print(a.ndim)

# print(a.size)

# print(a.dtype)

'''
索引
切片
'''
# print(a[2][1])
# print(a[:2])
# print(a[:, 0:2])  # 逗号左边是数组的第一个维度，右边是第二个维度
# print(a[:2, 0:2])

# print(a)
# print(a[::-1])  # 行倒置
# print(a[:, ::-1])  # 列倒置
# print(a[::-1, :-1])


