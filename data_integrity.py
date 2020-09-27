# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019
@author: 33888

Updated on Sun Sep  27 15:11:19 2020
@author: 50508

功能: 求该机组基于时间的数据完整度
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts；  
输出: data_integrity.csv（1*5） 
"""

from common.DBUtil import exec_sql
from common.ComputeUtil import time_diff

import datetime
import os
import sys
import pandas as pd

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
# 先引入目录的上级
sys.path.append(rootPath)

import config.property as CONFIG


class API_data_integrity(object):
    def __init__(self):
        # 数据库
        self.db = CONFIG.db
        # 表
        self.table = CONFIG.table
        # 输出目录
        self.result_dir = CONFIG.result_dir

    def dataProcess(self, date_start=[], date_end=[]):
        # 功能：求该机组基于时间的数据完整度
        # 输入：
        #   date_start——起始日期，如’2019-01-01’，若无，则默认为min(ts)；
        #   date_end——结束日期，如’2019-05-31’，若无，则默认为max(ts)
        # 输出：结果已保存至result_dir路径，并输出result

        # 数据准备
        # 1.where条件
        where_condition = "where wtid='632500001' and ts >= '2019-01-01 00:00:00' and ts < '2020-05-01 00:00:00' limit 100000"

        # 2.选择列
        result_column = "wfid,wtid,ts,WTUR_Other_Rn_I16_LimPow,WTUR_State_Rn_I8"

        # 3.分析数据准备
        sql = "select " + result_column + " from {0}" + where_condition.format(self.table)
        # 7s数据
        data = exec_sql(self.db, sql)

        # 处理数据
        result = pd.DataFrame(
            columns=['wfid', 'wtid', 'date_start', 'date_end', 'date_start_real', 'date_end_real', 'hour', 'line', 'data_integrity', 'sample_freq',
                     'limpow_percent', 'usable_percent'])
        data = time_diff(data, 'ts', flag=1)
        hour_actual = data['ts_diff'].sum() / 3600

        result.loc[0, 'wfid'] = data.loc[0, 'wfid']
        result.loc[0, 'wtid'] = data.loc[0, 'wtid']

        if len(date_start) != 0:
            result.loc[0, 'date_start'] = date_start
        else:
            date_start = data['ts'].min()[0:10]
        if len(date_end) != 0:
            result.loc[0, 'date_end'] = date_end
        else:
            date_end = data['ts'].max()[0:10]

        a = datetime.datetime.strptime(date_end, '%Y-%m-%d') - datetime.datetime.strptime(date_start, '%Y-%m-%d')
        hour_total = a.total_seconds() / 3600 + 24

        result.loc[0, 'date_start_real'] = data['ts'].min()[0:10]
        result.loc[0, 'date_end_real'] = data['ts'].max()[0:10]
        result.loc[0, 'hour'] = hour_actual
        result.loc[0, 'line'] = len(data)
        result.loc[0, 'data_integrity'] = hour_actual / hour_total
        result.loc[0, 'sample_freq'] = data['ts_diff'].mean()
        result.loc[0, 'limpow_percent'] = data['WTUR_Other_Rn_I16_LimPow'].sum() / len(data)
        result.loc[0, 'usable_percent'] = data['WTUR_State_Rn_I8'].sum() / len(data)
        result.to_csv(self.result_dir + '/' + str(data.loc[0, 'wtid']) + '_1_1_data_integrity.csv', index=False)
        return (result)


if __name__ == '__main__':
    instance = API_data_integrity()
    instance.dataProcess('2019-01-01', '2019-05-01')
