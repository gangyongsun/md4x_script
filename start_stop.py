# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019
@author: 33888

Updated on Sun Sep  27 15:11:19 2020
@author: 50508

功能：此程序用于启停机时长和次数统计
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts, WTUR_TurSt_Rs_S,WTUR_WSpd_Ra_F32等; 
输出: start_stop: 启停机时长统计：wfid, wtid, ts, 起/停机, 时长(s)
"""
from common.FunUtil import WindNorm_altitude
from common.ComputeUtil import time_diff
from common.ComputeUtil import state_recognize
from common.ComputeUtil import start_stop_extract
from common.ComputeUtil import start_2h_count
from common.DBUtil import exec_sql

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 先引入目录的上级
sys.path.append(rootPath)

import config.property as CONFIG


class API_start_stop(object):
    def __init__(self):
        # 数据库
        self.db = CONFIG.db

        # 表
        self.table = CONFIG.table

        # 输出目录
        self.result_dir = CONFIG.result_dir

    def plot(self, start_stop, start_2h, data, result_dir):
        # 绘图
        # 1
        plt.figure()
        plt.scatter(start_2h['wind_mean'], start_2h['count'], s=6, color='#4E79A7')
        plt.xlabel("2h wind mean [m/s]", fontproperties="STXihei")
        plt.ylabel("start count", fontproperties="STXihei")
        plt.grid()
        plt.show()
        plt.savefig(result_dir + '/' + str(data.loc[0, 'wtid']) + '_4_1_wind2h_count.png', dpi=300, bbox_inches='tight')
        plt.close()
        # 2
        start = start_stop[start_stop['state'] == 'start']
        plt.figure()
        plt.scatter(start['wind_mean'], start['seconds'], s=6, color='#4E79A7')
        plt.xlabel("wind [m/s]", fontproperties="STXihei")
        plt.ylabel("start duration [s]", fontproperties="STXihei")
        plt.grid()
        plt.show()
        plt.savefig(result_dir + '/' + str(data.loc[0, 'wtid']) + '_4_1_wind_start_duration.png', dpi=300, bbox_inches='tight')
        plt.close()
        # 3
        stop = start_stop[start_stop['state'] == 'stop']
        plt.figure()
        plt.scatter(stop['wind_mean'], stop['seconds'], s=6, color='#4E79A7')
        plt.xlabel("wind [m/s]", fontproperties="STXihei")
        plt.ylabel("stop duration [s]", fontproperties="STXihei")
        plt.grid()
        plt.show()
        plt.savefig(result_dir + '/' + str(data.loc[0, 'wtid']) + '_4_1_wind_stop_duration.png', dpi=300, bbox_inches='tight')
        plt.close()
        return ()

    def main_process(self, data, limit):
        # 1. 前期处理：根据风机状态将数据切割，取出时长和时间范围，并判断是否连续
        data = data.sort_values('ts')
        data = data.reset_index(drop=True)
        data = time_diff(data, 'ts')  # 加一列：ts_diff，异常值不能用round(mean)代替
        data_1 = state_recognize(data, 'WTUR_TurSt_Rs_S')
        result = data_1.groupby(['wfid', 'wtid', 'WTUR_TurSt_Rs_S', 'WTUR_TurSt_Rs_S_slice'])['ts_diff'].sum()
        result = pd.DataFrame(result)
        result['ts_diff_max'] = data_1.groupby(['wfid', 'wtid', 'WTUR_TurSt_Rs_S', 'WTUR_TurSt_Rs_S_slice'])['ts_diff'].max()
        result['ts_start'] = data_1.groupby(['wfid', 'wtid', 'WTUR_TurSt_Rs_S', 'WTUR_TurSt_Rs_S_slice'])['ts'].min()
        result['ts_end'] = data_1.groupby(['wfid', 'wtid', 'WTUR_TurSt_Rs_S', 'WTUR_TurSt_Rs_S_slice'])['ts'].max()
        result = result.reset_index()
        result['is_discontinue'] = [(1 if i > limit else 0) for i in result['ts_diff_max']]
        result = result.sort_values('WTUR_TurSt_Rs_S_slice')
        result = result.reset_index()
        result = result.drop('index', axis=1)
        result = result.rename(columns={'ts_diff': 'seconds'})
        # 2. 结果1：基于result统计起停机时长、时间范围、平均风速
        start_stop = start_stop_extract(result, data)  # 基于result取出起停机的时长、时间范围、平均风速
        start_stop.to_csv(self.result_dir + '/' + str(data.loc[0, 'wtid']) + '_5_1_start_stop_slice.csv', index=False)
        # 3. 结果2：基于result统计起停机时长、时间范围、平均风速
        start_stop_sta = start_stop.groupby(['wfid', 'wtid', 'state'])['wtid'].count()
        start_stop_sta = pd.DataFrame(start_stop_sta)
        start_stop_sta.columns = ['count']
        start_stop_sta['seconds_min'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds'].min()
        start_stop_sta['seconds_max'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds'].max()
        start_stop_sta['seconds_mean'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds'].mean()
        start_stop_sta['seconds_3_1_min'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_3_1'].min()
        start_stop_sta['seconds_3_1_max'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_3_1'].max()
        start_stop_sta['seconds_3_1_mean'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_3_1'].mean()
        start_stop_sta['seconds_3_2_min'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_3_2'].min()
        start_stop_sta['seconds_3_2_max'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_3_2'].max()
        start_stop_sta['seconds_3_2_mean'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_3_2'].mean()
        start_stop_sta['seconds_4_min'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_4'].min()
        start_stop_sta['seconds_4_max'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_4'].max()
        start_stop_sta['seconds_4_mean'] = start_stop.groupby(['wfid', 'wtid', 'state'])['seconds_4'].mean()
        start_stop_sta = start_stop_sta.reset_index()
        start_stop_sta.to_csv(self.result_dir + '/' + str(data.loc[0, 'wtid']) + '_5_1_start_stop_count.csv', index=False)
        # 4. 结果3：基于start_stop将时间按两小时切割，计算起机次数
        start_2h = start_2h_count(start_stop, data, self.result_dir)
        start_2h.to_csv(self.result_dir + '/' + str(data.loc[0, 'wtid']) + '_5_1_start_2h.csv', index=False)

        # plot(start_stop,start_2h,data,result_dir)

        return (start_stop)

    def dataProcess(self, limit=200, wind_is_correct=0, wtid_info=[]):
        # 功能：用于启停机时长统计
        # 输入：
        #   data——7s数据；
        #   result_dir——输出路径；
        #   limit——当时间间隔超过limit，则认为是间断点，不作统计；
        #   若wind_is_correct=1，则需输入wtid_info,否则只需输入data即可
        # 输出：结果已保存至result_dir路径，并输出result

        # 数据准备
        # 1.where条件
        where_condition = "where wtid='632500001' and ts >= '2019-01-01 00:00:00' and ts < '2020-05-01 00:00:00' limit 100000"

        # 2.选择列
        if wind_is_correct == 0:
            result_column = "wfid,wtid,ts,WTUR_WSpd_Ra_F32,WTPS_Ang_Ra_F32_blade1,WTUR_TurSt_Rs_S"
        else:
            result_column = "wfid,wtid,ts,WTUR_WSpd_Ra_F32,WTPS_Ang_Ra_F32_blade1,WTUR_TurSt_Rs_S,WTUR_Temp_Ra_F32"

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
            data['WTUR_TurSt_Rs_S'] = pd.to_numeric(data['WTUR_TurSt_Rs_S'])

        start_stop = self.main_process(data, limit)
        return (start_stop)


if __name__ == '__main__':
    instance = API_start_stop
    instance.dataProcess(limit=200, wind_is_correct=0, wtid_info=[])
