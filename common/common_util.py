import os
import math
import datetime

import pandas as pd
import numpy as np

import athena_helper as aws_helper

import matplotlib.pyplot as plt

from config.property import result_dir
from config.property import yaw_error_result


def genNumArray(start, end):
    """
    生成数组数组
    :param start: 开始数字
    :param end: 结束数字
    :return: 数字数组
    """
    result_array=[]
    for num in range(start, end+1, 1):
        result_array.append(num)
    return result_array

def wind_norm_altitude(altitude, temperature, wind_speed, density):
    """
    根据海拔和温度将风速标准化
    :param altitude:
    :param temperature:
    :param wind_speed:
    :param density:
    :return:
    """
    AirDen = density
    undernum = 1 + (1 / 273.15) * temperature
    upnum = 1.293 * 10 ** (-(altitude / (18400 * undernum)))
    air_density = upnum / undernum
    windnorm = wind_speed * (air_density / AirDen) ** (1 / 3)
    return (windnorm)

def compute_com(data_10min):
    """
    计算每仓符合度
    :param data_10min: 尚未剔除的10min数据,包含：wfid、wtid、WTUR_WSpd_Ra_F32、WTUR_PwrAt_Ra_F32、windbin、power（担保/设计功率）、flag(0保留1剔除)
    :return: 每仓符合度
    """

    data_10min = data_10min[data_10min['flag'] == 0]  # 剔除点
    data_10min = data_10min.drop('flag', axis=1)

    groupby_data_10min = data_10min.groupby(['wfid', 'wtid', 'windbin'])# 分仓

    windbin_com = groupby_data_10min.mean()# 求平均

    windbin_com['count'] = groupby_data_10min['WTUR_WSpd_Ra_F32'].count()
    windbin_com = windbin_com.reset_index()

    windbin_com = windbin_com.dropna()# 去掉不满足条件的风速仓
    windbin_com = windbin_com[windbin_com['count'] >= 3] # 去掉点数小于3的风速仓


    windbin_com['comformity'] = windbin_com['WTUR_PwrAt_Ra_F32'] / windbin_com['power']


    return (windbin_com)


def compute_k(data_10min):
    """
    计算K值
    :param data_10min: 尚未剔除的10min数据，包含：wfid、wtid、WTUR_WSpd_Ra_F32、WTUR_PwrAt_Ra_F32、windbin、power（担保/设计功率）、flag(0保留1剔除)
    :return: K值
    """

    # 算风频
    windbin_fre = data_10min.groupby(['wfid', 'wtid', 'windbin'])['WTUR_WSpd_Ra_F32'].count()  # 分仓求平均
    windbin_fre = pd.DataFrame(windbin_fre)
    windbin_fre.columns = ['num']
    windbin_fre = windbin_fre.reset_index()

    # 算功率曲线
    data_10min_del = data_10min[data_10min['flag'] == 0]  # 剔除点
    data_10min_del = data_10min_del.drop('flag', axis=1)
    windbin_com = data_10min_del.groupby(['wfid', 'wtid', 'windbin']).mean()  # 分仓求平均

    windbin_com['count'] = data_10min_del.groupby(['wfid', 'wtid', 'windbin'])['WTUR_WSpd_Ra_F32'].count()
    windbin_com = windbin_com.reset_index()

    windbin_com = windbin_com.dropna()  # 去掉不满足条件的风速仓

    windbin_com = windbin_com[windbin_com['count'] >= 3]  # 去掉点数小于3的风速仓
    windbin_com = windbin_com.drop('count', axis=1)

    # 计算k
    windbin_com = pd.merge(windbin_com, windbin_fre, how='left', on=['wfid', 'wtid', 'windbin'])
    windbin_com['actual_pow_sum'] = windbin_com['WTUR_PwrAt_Ra_F32'] * windbin_com['num']
    windbin_com['design_pow_sum'] = windbin_com['power'] * windbin_com['num']
    k = windbin_com['actual_pow_sum'].sum() / windbin_com['design_pow_sum'].sum()
    return (k)


def compute_capc(windbin_com):
    """
    计算capc
    :param windbin_com: 每仓符合度
    :return: capc
    """

    df = windbin_com.copy()
    df['wind_3'] = df['WTUR_WSpd_Ra_F32'] ** 3
    df['wind_3_com'] = df['wind_3'] * df['comformity']
    capc = df['wind_3_com'].sum() / df['wind_3'].sum()
    return (capc)


def time_diff(data, var, flag=0):
    """
    计算行与行之间秒级的时间差
    :param data: 数据集
    :param var: 指定的时间变量名(eg: ts/WTUR_Tm_Rw_Dt,可字符串可时间类型)
    :param flag: flag=0，异常时间差不做任何处理；flag=1，超过(mean*2)的时间差用round(mean)代替
    :return: 在原数据集的最后一列加一列*_diff, 输出结果已按时间排序，索引已重置，第一行的空值用第二个值代替
    """

    # 取出第一行的var列值
    sample_value = data.loc[data.index[0], var]

    # 判断是否为字符串，目的：转换字符串时间格式为timestamp格式
    if isinstance(sample_value, str):
        data['ts_1'] = pd.to_datetime(data[var], format='%Y-%m-%d %H:%M:%S')
    else:
        data['ts_1'] = data[var]

    # 对时间排序
    data = data.sort_values('ts_1')

    # 重新排序，并把之前的列index索引去掉
    data = data.reset_index(drop=True)

    # 定义列名
    var_output = var + '_diff'
    data[var_output] = data['ts_1'].diff()
    data[var_output] = [i.total_seconds() for i in data[var_output]]

    # 用第二个值代替第一个值
    data.loc[0, var_output] = data.loc[1, var_output]

    if flag == 1:
        ts_mean = data[var_output].mean()
        data.loc[data[var_output] > (ts_mean * 2), var_output] = round(ts_mean)

    # 删除ts_1列
    data = data.drop('ts_1', axis=1)
    return (data)


def state_recognize(df, var_name):
    """
    在输入的数据集上加一列：var_name_slice(每次状态切换的不重复标记)
    :param df: 数据集
    :param var_name: 需要做不重复标记的变量名(若var_name那一列是相同的值，则var_name_slice全为1)
    :return: df加一列var_name_slice
    """

    var_slice = var_name + '_slice'
    var_diff = var_name + '_diff_x'
    if len(df[var_name].unique()) == 1:  # 只有一种状态
        df[var_slice] = 1
    else:
        df[var_diff] = df[var_name].diff()
        df.loc[0, var_diff] = 0
        a = np.linspace(0, len(df) - 1, len(df))
        df['ID_1'] = a.reshape(len(df), 1)

        a = df.loc[df[var_diff] != 0, 'ID_1']
        a = a.reset_index()

        a = a.drop('index', axis=1)
        df[var_slice] = 0
        df.loc[0:int(a.loc[0] - 1), var_slice] = 1
        for i in range(0, len(a)):
            if i == (len(a) - 1):
                df.loc[int(a.loc[i]):(len(df) - 1), var_slice] = i + 2
            else:
                df.loc[int(a.loc[i]):int(a.loc[i + 1] - 1), var_slice] = i + 2
        df = df.drop([var_diff, 'ID_1'], axis=1)
    return (df)


def start_stop_extract(df, data):
    """
    基于df取出起停机的时长、时间范围、平均风速
    :param df: 每个风机状态一行统计结果，包含时间范围、时长、是否连续
    :param data: 7s数据，包含时间、风速
    :return: re——起停机的时长、时间范围、平均风速;pdblade_tor——风机状态为3和4时的变桨速率和扭矩反馈;起机提取：3-4-5，统计3和4的时长以及平均风速
    """

    re_1 = pd.DataFrame()
    for i in range(0, (len(df) - 2)):
        if (df.loc[i, 'WTUR_TurSt_Rs_S'] == 3) & (df.loc[(i + 1), 'WTUR_TurSt_Rs_S'] == 4) & (df.loc[(i + 2), 'WTUR_TurSt_Rs_S'] == 5) & (
                df.loc[[i, i + 1, i + 2], 'is_discontinue'].sum() == 0):
            ts_start = df.loc[i, 'ts_start']
            ts_end_1 = df.loc[i, 'ts_end']
            ts_end_2 = df.loc[(i + 1), 'ts_end']
            re_1_i = df.loc[[i], :]
            re_1_i = re_1_i[['wfid', 'wtid']]
            re_1_i['ts_start'] = ts_start
            re_1_i['ts_end'] = ts_end_2
            re_1_i['seconds'] = df.loc[i, 'seconds'] + df.loc[(i + 1), 'seconds']
            re_1_i['seconds_3'] = df.loc[i, 'seconds']
            re_1_i['seconds_3_1'] = data.loc[(data['ts'] >= ts_start) & (data['ts'] <= ts_end_1) & (data['WTPS_Ang_Ra_F32_blade1'] > 55), 'ts_diff'].sum()
            re_1_i['seconds_3_2'] = re_1_i['seconds_3'] - re_1_i['seconds_3_1']
            re_1_i['seconds_4'] = df.loc[(i + 1), 'seconds']
            re_1_i['wind_mean'] = data.loc[(data['ts'] >= ts_start) & (data['ts'] <= ts_end_2), 'WTUR_WSpd_Ra_F32'].mean()
            re_1_i['wind_mean_3_1'] = data.loc[
                (data['ts'] >= ts_start) & (data['ts'] <= ts_end_1) & (data['WTPS_Ang_Ra_F32_blade1'] > 55), 'WTUR_WSpd_Ra_F32'].mean()
            re_1_i['wind_mean_4'] = data.loc[(data['ts'] >= ts_end_1) & (data['ts'] <= ts_end_2), 'WTUR_WSpd_Ra_F32'].mean()
            re_1_i['state'] = 'start'
            re_1 = re_1.append(re_1_i)
    # 停机提取：5-1，统计1的时长以及平均风速
    re_2 = pd.DataFrame()
    for i in range(0, (len(df) - 1)):
        if (df.loc[i, 'WTUR_TurSt_Rs_S'] == 5) & (df.loc[(i + 1), 'WTUR_TurSt_Rs_S'] == 1) & (df.loc[[i, i + 1], 'is_discontinue'].sum() == 0):
            ts_start = df.loc[(i + 1), 'ts_start']
            ts_end = df.loc[(i + 1), 'ts_end']
            re_2_i = df.loc[[i + 1], :]
            re_2_i['wind_mean'] = data.loc[(data['ts'] >= ts_start) & (data['ts'] <= ts_end), 'WTUR_WSpd_Ra_F32'].mean()
            re_2_i['state'] = 'stop'
            re_2_i = re_2_i[['wfid', 'wtid', 'ts_start', 'ts_end', 'seconds', 'wind_mean', 'state']]
            re_2 = re_2.append(re_2_i)

    re = pd.concat([re_1, re_2], axis=0)
    re = re.sort_values('ts_start')
    re = re.reset_index()
    re = re.drop('index', axis=1)
    re = re[
        ['wfid', 'wtid', 'ts_start', 'ts_end', 'seconds', 'seconds_3', 'seconds_3_1', 'seconds_3_2', 'seconds_4', 'wind_mean', 'wind_mean_3_1', 'wind_mean_4',
         'state']]
    return (re)


def start_2h_count(start_stop, data):
    """
    基于start_stop将时间按两小时切割，计算起机次数
    :param start_stop: 起停机时长、时间范围、平均风速
    :param data: 原始7s数据
    :return: start_2h
    """

    # 1. 对start_stop的时间进行划分，统计次数
    start_stop = start_stop[start_stop['state'] == 'start']
    start_stop['date'] = start_stop['ts_start'].str[0:10]
    start_stop['ts_start'] = pd.to_datetime(start_stop['ts_start'], format='%Y-%m-%d %H:%M:%S')
    start_stop['hour'] = [i.hour for i in start_stop['ts_start']]  # 取出小时
    start_stop['ID'] = [math.floor(i / 2) * 2 for i in start_stop['hour']]  # 对小时做变换
    result_1 = start_stop.groupby(['wfid', 'wtid', 'date', 'ID'])['hour'].count()
    result_1 = pd.DataFrame(result_1)
    result_1.columns = ['count']
    result_1 = result_1.reset_index()
    # 2. 对data的时间进行划分，统计平均风速
    data['date'] = data['ts'].str[0:10]
    data['ts'] = pd.to_datetime(data['ts'], format='%Y-%m-%d %H:%M:%S')
    data['hour'] = [i.hour for i in data['ts']]  # 取出小时
    data['ID'] = [math.floor(i / 2) * 2 for i in data['hour']]  # 对小时做变换
    result_2 = data.groupby(['wfid', 'wtid', 'date', 'ID'])['WTUR_WSpd_Ra_F32'].mean()
    result_2 = pd.DataFrame(result_2)
    result_2.columns = ['wind_mean']
    result_2 = result_2.reset_index()

    re = pd.merge(result_1, result_2, how='right', on=['wfid', 'wtid', 'date', 'ID'])
    re = re.fillna(0)
    re['date'] = pd.to_datetime(re['date'], format='%Y-%m-%d')
    re['ts_start'] = [
        datetime.datetime(re.loc[i, 'date'].year, re.loc[i, 'date'].month, re.loc[i, 'date'].day, int(re.loc[i, 'ID'])).strftime('%Y-%m-%d %H:%M:%S') for i in
        re.index]
    re = re[['wfid', 'wtid', 'ts_start', 'count', 'wind_mean']]
    re = re.sort_values('ts_start')
    re = re.reset_index()
    re = re.drop('index', axis=1)

    return (re)


def yawerrorcal(df):
    wfid = data['wfid'].iloc[0]
    wtid = data['wtid'].iloc[0]
    # df=dataset
    cutinwind = 3
    cutoutwind = 25
    efcutoutwind = 7
    windstep = 0.5

    windbinno = int((cutoutwind - cutinwind) / windstep + 1)
    efwindbinno = int((efcutoutwind - cutinwind) / windstep + 1)
    windbin = np.linspace(3, 8, 11)
    yaw_bin = np.linspace(-30, 29.8, num=300)

    efwindbin = np.linspace(cutinwind, efcutoutwind, num=efwindbinno)

    wind_dir_bin = np.zeros((efwindbinno, 300))
    fit_power_db = np.zeros((efwindbinno, 300))
    power_std = np.zeros((efwindbinno, 9))
    power_avg = np.zeros((efwindbinno, 9))
    power_std_r = np.zeros((efwindbinno, 9))
    power_avg_r = np.zeros((efwindbinno, 9))
    yawerror = np.zeros(efwindbinno + 1)
    maxpower = np.zeros(windbinno + 1)
    validdata = np.zeros(efwindbinno + 1)

    for iwind in range(1, efwindbinno + 1):
        wind_speed = (iwind - 1) * 0.5 + cutinwind
        # print(wind_speed)
        tempwindbin = df[(df['WTUR_WSpd_Ra_F32'] > wind_speed - 0.25) & (df['WTUR_WSpd_Ra_F32'] <= wind_speed + 0.25)]
        validdata[iwind - 1] = round(len(tempwindbin) * 7 / 3600, 2)

        for iwdir in range(1, 301):
            tempdirbin = tempwindbin[(tempwindbin['WYAW_Wdir_Ra_F32'] > (iwdir - 1) * 0.2 - 30) & (tempwindbin['WYAW_Wdir_Ra_F32'] <= iwdir * 0.2 - 30)]
            wind_dir_bin[iwind - 1][iwdir - 1] = np.nanmean(tempdirbin['WTUR_PwrAt_Ra_F32'])

        fitpara = np.polyfit(yaw_bin[~np.isnan(wind_dir_bin[iwind - 1])], wind_dir_bin[iwind - 1][~np.isnan(wind_dir_bin[iwind - 1])], 2)
        fitpower = np.polyval(fitpara, yaw_bin)
        yawerror[iwind - 1] = yaw_bin[np.where(fitpower == np.max(fitpower))]
        maxpower[iwind - 1] = np.max(fitpower)
        yaw_error = yawerror[iwind - 1]
        fit_power_db[iwind - 1] = fitpower

        num_of_step = 10
        for step in np.arange(1, num_of_step, 1):
            power_avg[iwind - 1][step - 1] = np.nanmean(wind_dir_bin[iwind - 1][(90 - step * 10):(90 - (step - 1) * 10)])
            power_std[iwind - 1][step - 1] = np.nanstd(wind_dir_bin[iwind - 1][(90 - step * 10):(90 - (step - 1) * 10)])
            power_avg_r[iwind - 1][step - 1] = np.nanmean(wind_dir_bin[iwind - 1][(220 - step * 10):(220 - (step - 1) * 10)])
            power_std_r[iwind - 1][step - 1] = np.nanstd(wind_dir_bin[iwind - 1][(220 - step * 10):(220 - (step - 1) * 10)])
        if (yaw_error > (-14.0)) & (yaw_error < 14.0):
            continue
        elif yaw_error <= -14.0:
            for j in np.arange(1, num_of_step - 2, 1):
                if (power_avg[iwind - 1][j] >= power_avg[iwind - 1][j - 1]) & (power_avg[iwind - 1][j] >= power_avg[iwind - 1][j + 1]):
                    yawerror[iwind - 1] = -15.0 - (j - 1) * 2
                    break
                elif (power_avg[iwind - 1][j] >= power_avg[iwind - 1][j - 1]) & (power_std[iwind - 1][j] <= power_std[iwind - 1][j + 1]):
                    yawerror[iwind - 1] = -15.0 - (j - 1) * 2
                    break
                else:
                    continue
        elif yaw_error >= 14.0:
            for j in np.arange(1, num_of_step - 2, 1):
                if (power_avg_r[iwind - 1][j] >= power_avg_r[iwind - 1][j - 1]) & (power_avg_r[iwind - 1][j] >= power_avg_r[iwind - 1][j + 1]):
                    yawerror[iwind - 1] = 15.0 + (j - 1) * 2
                    break
                elif (power_avg_r[iwind - 1][j] >= power_avg_r[iwind - 1][j - 1]) & (power_std_r[iwind - 1][j] <= power_std_r[iwind - 1][j + 1]):
                    yawerror[iwind - 1] = 15.0 + (j - 1) * 2
                    break
                else:
                    continue
    plt.figure(figsize=(12, 6))

    for i in np.arange(1, 10, 1):
        plt.subplot(3, 3, i)
        max_power = np.linspace(maxpower[i - 1] - 20 * ((3 + (i - 1) * 0.5) / 3) ** 3, maxpower[i - 1] + 60 * ((3 + (i - 1) * 0.5) / 3) ** 3, 8)
        yaw_error_array = np.array([yawerror[i - 1]] * 8)
        plt.scatter(yaw_bin, wind_dir_bin[i - 1][0:300], c="b", marker=".")
        plt.plot(yaw_bin, fit_power_db[i - 1], "r-")
        plt.plot(yaw_error_array, max_power, "r--")
        plt.xlabel("wind direction[deg]")
        plt.ylabel("power[kW] " + str(windbin[i - 1]) + 'm/s')
        # plt.title(str(wsp)+"m/s  "+str(yawerror[i-1])+"deg")
    filename = str(wtid) + "_4_4_yaw_error.png"
    savename = os.path.join(result_dir + yaw_error_result, filename)
    aws_helper.save_png_aws(plt, savename, dpi=300)
    plt.close()

    validdata[efwindbinno] = sum(validdata)
    yawerror[efwindbinno] = np.dot(np.power(efwindbin, 3), yawerror[0:efwindbinno]) / sum(np.power(efwindbin, 3))
    yawerrRlt = pd.DataFrame({"windbin": np.concatenate((efwindbin, np.array([np.nan])), axis=0), "Duration[h]": validdata, "YawError[deg]": yawerror})
    yawerrRlt['wfid'] = wfid
    yawerrRlt['wtid'] = wtid

    return (yawerrRlt)

    print(yawerrRlt.head())
    yawerrRlt.columns = ['windbin', 'Duration', 'YawError', 'wfid', 'wtid']
    yawerrRlt.iloc[:-1, :].to_csv(os.path.join(result_dir + yaw_error_result, str(wtid) + '_4_4_yaw_error_windbin.csv'), index=False)
    yawerrRlt.iloc[-1, :].to_frame().T[['Duration', 'YawError', 'wfid', 'wtid']].to_csv(
        os.path.join(result_dir + yaw_error_result, str(wtid) + '_4_4_yaw_error_sum.csv'), index=False)
    return ()