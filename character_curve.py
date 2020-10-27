# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019
@author: 33888

Updated on Sun Sep  27 15:11:19 2020
Updated on Sun Oct  20 13:38:22 2020
@author: 50508

功能: 求该机组的特性曲线、特性曲线散点图
输入: 涉及数据为:
    1) 7s数据变量
    2) 各风场海拔、空气密度(用于将风速矫正)
输出: character_curve.csv（n*11）
"""

from common.common_util import wind_norm_altitude
from common.db_util import exec_sql
from config.property import db
from config.property import table
from config.property import result_dir
from config.property import character_curve_result
import matplotlib.pyplot as plt
import athena_helper as aws_helper


def plot(data_7s, data_10min, data_curve):
    """
    绘图：7s散点+实际曲线，10min散点+实际曲线，已剔除异常值
    :param data_7s: 7s数据
    :param data_10min: 10Min数据
    :param data_curve: 拟合曲线数据
    :return:
    """

    data_1 = data_7s[data_7s['WTUR_State_Rn_I8'] == 1]

    # 1 风速-功率
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WTUR_PwrAt_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("power [kW]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_1_win_pow_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WTUR_PwrAt_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("power [kW]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_1_win_pow_10min.png', dpi=300)
    plt.close()

    # 2 风速-转速
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WGEN_Spd_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("generator speed [rpm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_2_win_gen_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WGEN_Spd_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("generator speed [rpm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_2_win_gen_10min.png', dpi=300)
    plt.close()

    # 3 风速-扭矩
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_3_win_tor_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_3_win_tor_10min.png', dpi=300)
    plt.close()

    # 4 转速-扭矩
    plt.figure()
    plt.scatter(data_1['WGEN_Spd_Ra_F32'], data_1['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("generator speed [rpm]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_4_gen_tor_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WGEN_Spd_Ra_F32'], data_10min['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("generator speed [rpm]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_4_gen_tor_10min.png', dpi=300)
    plt.close()

    # 5 风速-桨距角
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTPS_Ang_Ra_F32_blade1'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("pitch angle [deg]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_5_win_pit_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['windbin'], data_curve['WTPS_Ang_Ra_F32_blade1'], color='#E15759')
    plt.scatter(data_curve['windbin'], data_curve['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("pitch angle [deg]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_5_win_pit_10min.png', dpi=300)
    plt.close()

def main_process(data_7s, data_10min):
    """
    求机组的特性曲线和特性曲线散点图
    :param data_7s: 7s数据
    :param data_10min: 10min数据
    :return:
    """

    # 数据处理
    # data_10min['windbin'] = round(data_10min['WTUR_WSpd_Ra_F32'] / 0.5 + 0.00000001) * 0.5
    data_10min = data_10min.reset_index()

    data_avg = data_10min.groupby(['wfid', 'wtid', 'windbin']).mean()  # 分仓求平均
    data_avg = data_avg.drop(['WTUR_State_Rn_I8', 'count'], axis=1)  # 删除列
    data_avg['count'] = data_10min.groupby(['wfid', 'wtid', 'windbin'])['WTUR_WSpd_Ra_F32'].count()
    data_avg = data_avg.reset_index()
    # 保存文件
    data_avg.to_csv(result_dir + '/' + str(data_7s.loc[0, 'wtid']) + '_3_1_character_curve.csv', index=False)
    # 调用绘图功能函数
    plot(data_7s, data_10min, data_avg)


def dataProcess(wind_is_correct=0, wtid_info=[]):
    wtid_data = "632500001"
    start_time = "2019-01-01 00:00:00"
    end_time = "2019-12-31 00:00:00"

    # 基本where条件
    condition_where = " where wtid= '" + wtid_data + "' and ts >= '" + start_time + "' and ts < '" + end_time + "'"  # and WTUR_State_Rn_I8=1 "
    # condition_where = " where wtid >= '632500001' and wtid<='632500010' and ts >= '" + start_time + "' and ts < '" + end_time + "' and WTUR_State_Rn_I8=1"

    # 7s数据基本列
    column_7s = "wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WGEN_Spd_Ra_F32, WCNV_Other_Ra_F32_TorqueReference, WTPS_Ang_Ra_F32_blade1, WTUR_State_Rn_I8"

    if wind_is_correct != 0:
        column_7s = column_7s + ", WTUR_Temp_Ra_F32"

    # 10min时间列
    column_10min_ts = "concat(substring(ts,1,15),'0:00') AS ts_2"

    sql_7s = "SELECT " + column_7s + " from {0} " + condition_where

    sql_7s_with_10min_column = "SELECT " + column_7s + "," + column_10min_ts + " from {0} " + condition_where
    sql_10min_column1 = "wfid, wtid, ts_2, WTUR_State_Rn_I8, WTUR_WSpd_Ra_F32,round(WTUR_WSpd_Ra_F32/0.5+ 0.00000001)*0.5 as windbin, WTUR_PwrAt_Ra_F32,WGEN_Spd_Ra_F32,WCNV_Other_Ra_F32_TorqueReference,WTPS_Ang_Ra_F32_blade1, count"
    sql_10min_column2 = "wfid, wtid, ts_2, AVG(WTUR_State_Rn_I8) as WTUR_State_Rn_I8, AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32, AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32, AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference , AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1, count(WTUR_WSpd_Ra_F32) as count"
    sql_10min = "select " + sql_10min_column1 + " from ( select " + sql_10min_column2 + " from ( " + sql_7s_with_10min_column + " ) t  GROUP BY(wfid, wtid, ts_2)  ) t2 where WTUR_State_Rn_I8 > 0.9 and count > 30"

    # 执行SQL获取数据
    sql_7s = sql_7s.format(table)
    sql_10min = sql_10min.format(table)

    data_7s = aws_helper.execute_query_aws(db, sql_7s)
    data_10min = aws_helper.execute_query_aws(db, sql_10min)

    # wind_is_correct不为0的情况
    if wind_is_correct != 0:
        sql_7s_with_10min_column = sql_7s_with_10min_column.format(table)
        data_7s = exec_sql(db, sql_7s_with_10min_column)

        wtid = data_7s.loc[0, 'wtid']

        # wtid_info表
        wtid_info_i = wtid_info[wtid_info['wtid'] == wtid]
        wtid_info_i = wtid_info_i.reset_index()
        wtid_info_i = wtid_info_i.drop('index', axis=1)
        altitude = wtid_info_i.loc[0, 'altitude']
        density = wtid_info_i.loc[0, 'density']

        data_7s['WTUR_WSpd_Ra_F32'] = wind_norm_altitude(altitude, data_7s['WTUR_Temp_Ra_F32'], data_7s['WTUR_WSpd_Ra_F32'], density)  # 风速折到density下

        data_10min = data_7s.groupby(['wfid', 'wtid', 'ts_2']).mean()  # 7s转10Min
        data_10min['count'] = data_7s.groupby(['wfid', 'wtid', 'ts_2'])['WTUR_WSpd_Ra_F32'].count()
        data_10min = data_10min[(data_10min['WTUR_State_Rn_I8'] > 0.9) & (data_10min['count'] > 30)]
        data_10min['windbin'] = round(data_10min['WTUR_WSpd_Ra_F32'] / 0.5 + 0.00000001) * 0.5
        data_10min = data_10min.reset_index()

    main_process(data_7s, data_10min)


dataProcess(0)