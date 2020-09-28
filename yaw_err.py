# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:55:44 2020
@author: 32963

Updated on Sun Sep  27 15:11:19 2020
@author: 50508

功能: 求该机组的对风偏差
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32，WYAW_Wdir_Ra_F32，WTUR_State_Rn_I8，WTPS_Ang_Ra_F32_blade1；  
输出: 1)aw_error_windbin.csv (9*5) 2)yaw_error_sum.csv(1*4) 3)对风偏差统计图 
"""

from common.DBUtil import exec_sql
from config.property import db
from config.property import table

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def yawerrorcal(data, wfid, wtid):
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
        print(wind_speed)
        tempwindbin = data[(data['WTUR_WSpd_Ra_F32'] > wind_speed - 0.25) & (data['WTUR_WSpd_Ra_F32'] <= wind_speed + 0.25)]
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
    plt.close()

    validdata[efwindbinno] = sum(validdata)
    yawerror[efwindbinno] = np.dot(np.power(efwindbin, 3), yawerror[0:efwindbinno]) / sum(np.power(efwindbin, 3))
    yawerrRlt = pd.DataFrame({"windbin": np.concatenate((efwindbin, np.array([np.nan])), axis=0), "Duration[h]": validdata, "YawError[deg]": yawerror})

    yawerrRlt['wfid'] = wfid
    yawerrRlt['wtid'] = wtid

    yawerrRlt.columns = ['Duration', 'YawError', 'windbin', 'wfid', 'wtid']


def main_process(data):
    # 功能：求该机组的对风偏差
    # 输入：data——7s数据

    # 数据处理
    wfid = data['wfid'].iloc[0]
    wtid = data['wtid'].iloc[0]
    data = data.loc[(data['WTUR_State_Rn_I8'] == 1) & (data['WTPS_Ang_Ra_F32_blade1'] < 2),]
    yawerrorcal(data, wfid, wtid)


def dataProcess():
    # 功能：求该机组的对风偏差

    # 数据准备
    # 1.where条件
    where_condition = "where wtid='632500001' and ts >= '2019-01-01 00:00:00' and ts < '2020-05-01 00:00:00'"

    # 2.选择列
    result_column = "wfid,wtid,ts, WTUR_WSpd_Ra_F32,WTUR_PwrAt_Ra_F32,WYAW_Wdir_Ra_F32,WTUR_State_Rn_I8,WTPS_Ang_Ra_F32_blade1"

    # 3.SQL
    sql = "select " + result_column + " from {0} " + where_condition
    sql = sql.format(table)

    # 执行查询获取7s数据
    data = exec_sql(db, sql)
    main_process(data)


dataProcess()
