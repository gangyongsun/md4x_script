# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019
@author: 33888

Updated on Sun Sep  27 15:11:19 2020
@author: 50508

功能: 求该机组的特性曲线、特性曲线散点图
输入: 涉及数据为:
    1) 7s数据变量
    2) 各风场海拔、空气密度(用于将风速矫正)
输出: character_curve.csv（n*11）
"""

from common.FunUtil import WindNorm_altitude
from common.FunUtil import draw
from common.FunUtil import draw_ext
from common.DBUtil import exec_sql

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 先引入目录的上级
sys.path.append(rootPath)

import config.property as CONFIG


class API_Character_Curve(object):
    def __init__(self):
        # 数据库
        self.db = CONFIG.db

        # 表
        self.table = CONFIG.table

        # 输出目录
        self.result_dir = CONFIG.result_dir

        # 颜色
        self.dark_blue = CONFIG.dark_blue
        self.dark_red = CONFIG.dark_red

        # 字体
        self.font_STXihei = CONFIG.font_STXihei

        # X\Y Label
        self.lable_wind = CONFIG.lable_wind
        self.lable_power = CONFIG.lable_power
        self.lable_generator_speed = CONFIG.lable_generator_speed
        self.lable_torque_reference = CONFIG.lable_torque_reference
        self.lable_pitch_angle = CONFIG.lable_pitch_angle


    def plot(self, data, result, result_2):
        # 执行绘图：
        #   7s散点+实际曲线；
        #   10min散点+实际曲线，已剔除异常值；
        # 输入：
        #   data：       7s数据；
        #   result：     10Min数据；
        #   result_2：   拟合曲线

        # WTUR_State_Rn_I8：数据可用状态
        data_1 = data[data['WTUR_State_Rn_I8'] == 1]

        # 保存文件名头、7s文件尾、10min文件尾
        file_name_head = self.result_dir + '/' + str(data.loc[0, 'wtid'])
        file_name_tail_7s = '7s.png'
        file_name_tail_10min = '10min.png'

        # 1.风速-功率
        column_list = ['WTUR_WSpd_Ra_F32', 'WTUR_PwrAt_Ra_F32']
        save_file_name_part1 = file_name_head + '_3_1_1_win_pow_'
        # 1.1.风速-功率-7s
        draw(data_1, result_2, column_list, self.lable_wind, self.lable_power, save_file_name_part1 + file_name_tail_7s)
        # 1.2.风速-功率-10min
        draw(result, result_2, column_list, self.lable_wind, self.lable_power, save_file_name_part1 + file_name_tail_10min)

        # 2.风速-转速
        column_list = ['WTUR_WSpd_Ra_F32', 'WGEN_Spd_Ra_F32']
        save_file_name_part1 = file_name_head + '_3_1_2_win_gen_'
        # 2.1. 风速-转速-7s
        draw(data_1, result_2, column_list, self.lable_wind, self.lable_generator_speed, save_file_name_part1 + file_name_tail_7s)
        # 2.1. 风速-转速-10min
        draw(result, result_2, column_list, self.lable_wind, self.lable_generator_speed, save_file_name_part1 + file_name_tail_10min)

        # 3.风速-扭矩
        column_list = ['WTUR_WSpd_Ra_F32', 'WCNV_Other_Ra_F32_TorqueReference']
        save_file_name_part1 = file_name_head + '_3_1_3_win_tor_'
        # 3.1.风速-扭矩
        draw(data_1, result_2, column_list, self.lable_wind, self.lable_torque_reference, save_file_name_part1 + file_name_tail_7s)
        # 3.2.风速-扭矩
        draw(result, result_2, column_list, self.lable_wind, self.lable_torque_reference, save_file_name_part1 + file_name_tail_10min)

        # 4.转速-扭矩
        column_list = ['WGEN_Spd_Ra_F32', 'WCNV_Other_Ra_F32_TorqueReference']
        save_file_name_part1 = file_name_head + '_3_1_4_gen_tor_'
        # 4.1.转速-扭矩
        draw(data_1, result_2, column_list, self.lable_generator_speed, self.lable_torque_reference, save_file_name_part1 + file_name_tail_7s)
        # 4.2.转速-扭矩
        draw(result, result_2, column_list, self.lable_generator_speed, self.lable_torque_reference, save_file_name_part1 + file_name_tail_10min)

        # 5.风速-桨距角
        column_list = ['WTUR_WSpd_Ra_F32', 'WTPS_Ang_Ra_F32_blade1', 'windbin']
        save_file_name_part1 = file_name_head + '_3_1_5_win_pit_'
        # 5.1.风速-桨距角
        draw(data_1, result_2, column_list, self.lable_wind, self.lable_pitch_angle, save_file_name_part1 + file_name_tail_7s)
        # 5.2.风速-桨距角
        draw_ext(result, result_2, column_list, self.lable_wind, self.lable_pitch_angle, save_file_name_part1 + file_name_tail_10min)

    def main_process(self, data):
        # 功能：求该机组的特性曲线和特性曲线散点图
        # 输入：data——7s数据；result_dir——输出路径
        # 输出：结果已保存至result_dir路径，并输出result

        # 数据处理
        data['ts_2'] = data['ts'].str[0:10] + ' ' + data['ts'].str[11:15] + '0:00'
        result = data.groupby(['wfid', 'wtid', 'ts_2']).mean()  # 7s转10Min
        result['count'] = data.groupby(['wfid', 'wtid', 'ts_2'])['WTUR_WSpd_Ra_F32'].count()
        result = result[(result['WTUR_State_Rn_I8'] > 0.9) & (result['count'] > 30)]
        result['windbin'] = round(result['WTUR_WSpd_Ra_F32'] / 0.5 + 0.00000001) * 0.5
        result = result.reset_index()

        result_2 = result.groupby(['wfid', 'wtid', 'windbin']).mean()  # 分仓求平均
        result_2 = result_2.drop(['WTUR_State_Rn_I8', 'count'], axis=1)  # 删除列
        result_2['count'] = result.groupby(['wfid', 'wtid', 'windbin'])['WTUR_WSpd_Ra_F32'].count()
        result_2 = result_2.reset_index()

        result_2.to_csv(self.result_dir + '/' + str(data.loc[0, 'wtid']) + '_3_1_character_curve.csv', index=False)

        # 调用绘图功能函数
        self.plot(data, result, result_2)


    def dataProcess(self, wind_is_correct=0, wtid_info=[]):
        # 准备分析数据
        # 1.where条件
        where_condition = "where wtid='632500001' and ts >= '2019-01-01 00:00:00' and ts < '2020-05-01 00:00:00' limit 100000"

        # 2.选择列
        if wind_is_correct == 0:
            result_column = "wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WGEN_Spd_Ra_F32, WCNV_Other_Ra_F32_TorqueReference, WTPS_Ang_Ra_F32_blade1, WTUR_State_Rn_I8"
        else:
            result_column = "wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WGEN_Spd_Ra_F32, WCNV_Other_Ra_F32_TorqueReference, WTPS_Ang_Ra_F32_blade1," \
                            "WTUR_State_Rn_I8, WTUR_Temp_Ra_F32wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WGEN_Spd_Ra_F32, WCNV_Other_Ra_F32_TorqueReference, WTPS_Ang_Ra_F32_blade1," \
                            "WTUR_State_Rn_I8, WTUR_Temp_Ra_F32"

        # 3.分析数据准备
        sql = "select " + result_column + " from {0}" + where_condition.format(self.table)
        data = exec_sql(self.db, sql)

        # wind_is_correct不为0的情况
        if wind_is_correct != 0:
            wtid = data.loc[0, 'wtid']
            # wtid_info表
            wtid_info_i = wtid_info[wtid_info['wtid'] == wtid]
            wtid_info_i = wtid_info_i.reset_index()
            wtid_info_i = wtid_info_i.drop('index', axis=1)
            altitude = wtid_info_i.loc[0, 'altitude']
            density = wtid_info_i.loc[0, 'density']
            data['WTUR_WSpd_Ra_F32'] = WindNorm_altitude(altitude, data['WTUR_Temp_Ra_F32'], data['WTUR_WSpd_Ra_F32'], density)  # 风速折到density下

        self.main_process(data)


if __name__ == '__main__':
    instance = API_Character_Curve()
    instance.dataProcess()
