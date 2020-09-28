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
from config.property import db
from config.property import table
from datetime import datetime

import pandas as pd


def dataProcess(date_start=[], date_end=[]):
    # 功能：求该机组基于时间的数据完整度
    # 输入：
    #   date_start——起始日期，如’2019-01-01’，若无，则默认为min(ts)；
    #   date_end——结束日期，如’2019-05-31’，若无，则默认为max(ts)

    # 数据准备
    # 1.where条件
    where_condition = "where wtid='632500001' and ts >= '2019-01-01 00:00:00' and ts < '2020-05-01 00:00:00'"

    # 2.选择列
    result_column = "wfid,wtid,ts,WTUR_Other_Rn_I16_LimPow,WTUR_State_Rn_I8"

    # 3.分析数据准备
    sql = "select " + result_column + " from {0} " + where_condition
    sql = sql.format(table)

    # 7s数据
    data = exec_sql(db, sql)

    # 处理数据
    columns = ['wfid', 'wtid', 'date_start', 'date_end', 'date_start_real', 'date_end_real', 'hour', 'line', 'data_integrity', 'sample_freq', 'limpow_percent',
               'usable_percent']
    result = pd.DataFrame(columns=columns)

    data = time_diff(data, 'ts', flag=1)
    hour_actual = data['ts_diff'].sum() / 3600

    result.loc[0, 'wfid'] = data.loc[0, 'wfid']
    result.loc[0, 'wtid'] = data.loc[0, 'wtid']

    if len(date_start) != 0:
        result.loc[0, 'date_start'] = date_start
    else:
        date_start = data['ts'].min()[0:10]  # 取日期列最小值的年月日(例如2019-04-02)

    if len(date_end) != 0:
        result.loc[0, 'date_end'] = date_end
    else:
        date_end = data['ts'].max()[0:10]  # 取日期列最大值的年月日(例如2019-04-02)

    a = datetime.strptime(date_end, '%Y-%m-%d') - datetime.strptime(date_start, '%Y-%m-%d')
    hour_total = a.total_seconds() / 3600 + 24

    result.loc[0, 'date_start_real'] = data['ts'].min()[0:10]
    result.loc[0, 'date_end_real'] = data['ts'].max()[0:10]
    result.loc[0, 'hour'] = hour_actual
    result.loc[0, 'line'] = len(data)
    result.loc[0, 'data_integrity'] = hour_actual / hour_total
    result.loc[0, 'sample_freq'] = data['ts_diff'].mean()
    result.loc[0, 'limpow_percent'] = data['WTUR_Other_Rn_I16_LimPow'].sum() / len(data)
    result.loc[0, 'usable_percent'] = data['WTUR_State_Rn_I8'].sum() / len(data)
    return (result)


dataProcess('2019-03-23', '2019-12-30')
