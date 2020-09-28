#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 10:09
# @Author  : yonggang
# @Software: PyCharm
import numpy as np
from numpy import array  # 从numpy中引入array，为创建矩阵做准备

A = array([[1, 2, 3],  # 创建一个4行3列的矩阵
           [4, 5, 6],
           [7, 8, 9],
           [10, 11, 12]])

B = A.min(0)  # 返回A每一列最小值组成的一维数组；
print(B)  # 结果 ：[1 2 3]

B = A.min(1)  # 返回A每一行最小值组成的一维数组；
print(B)  # 结果 ：[ 1  4  7 10]

B = A.max(0)  # 返回A每一列最大值组成的一维数组；
print(B)  # 结果 ：[10 11 12]

B = A.max(1)  # 返回A每一行最大值组成的一维数组；
print(B)  # 结果 ：[ 3  6  9 12]

B = A.max()
print(B)

X = np.array([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19]])
print(X[:, 0])
print(X[:, 1])
print(X[1, :])

X = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20]])
print(X[:, 1:3])
