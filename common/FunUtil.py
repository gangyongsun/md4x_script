import matplotlib.pyplot as plt
from config.property import dark_red
from config.property import dark_blue
from config.property import font_STXihei

def WindNorm_altitude(altitude, tem, wind, densi):
    # 根据海拔和温度将风速标准化
    AirDen = densi
    undernum = 1 + (1 / 273.15) * tem
    upnum = 1.293 * 10 ** (-(altitude / (18400 * undernum)))
    airdensity = upnum / undernum
    windnorm = wind * (airdensity / AirDen) ** (1 / 3)
    return (windnorm)

def draw(data_1, data_2, column_list, x_label, y_label):
    # 绘图函数
    # column_list：colunm列表
    # x_label：x轴名；
    # y_label：y轴名；
    # 1.风速-功率
    # 创建窗口（Figure：面板(图)，matplotlib中的所有图像都是位于figure对象中，一个图像只能有一个figure对象）
    plt.figure()

    plt.scatter(data_1[column_list[0]], data_1[column_list[1]], s=0.5, color=dark_blue)
    plt.plot(data_2[column_list[0]], data_2[column_list[1]], color=dark_red)
    plt.scatter(data_2[column_list[0]], data_2[column_list[1]], s=0.5, color=dark_red)

    plt.xlabel(x_label, fontproperties=font_STXihei)
    plt.ylabel(y_label, fontproperties=font_STXihei)

    plt.grid()
    plt.show()
    plt.close()

def draw_ext(data_1, data_2, column_list, x_label, y_label):
    # 绘图函数扩展
    # column_list：colunm列表
    # x_label：x轴名；
    # y_label：y轴名；
    # 1.风速-功率
    # 创建窗口（Figure：面板(图)，matplotlib中的所有图像都是位于figure对象中，一个图像只能有一个figure对象）
    plt.figure()

    plt.scatter(data_1[column_list[0]], data_1[column_list[1]], s=0.5, color=dark_blue)
    plt.plot(data_2[column_list[2]], data_2[column_list[1]], color=dark_red)
    plt.scatter(data_2[column_list[2]], data_2[column_list[1]], s=0.5, color=dark_red)

    plt.xlabel(x_label, fontproperties=font_STXihei)
    plt.ylabel(y_label, fontproperties=font_STXihei)

    plt.grid()
    plt.show()
    plt.close()
