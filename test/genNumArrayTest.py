def genNumArray(start, end):
    """
    生成数组数组
    :param start: 开始数字
    :param end: 结束数字
    :return: 数组
    """
    result_array = []
    for num in range(start, end + 1, 1):
        result_array.append(str(num))
    return result_array


print(genNumArray(632500001, 632500050))
