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

from common.db_util import prepare_data
import athena_helper as aws_helper

from common.common_util import time_diff

from config.property import db
from config.property import table

from datetime import datetime
import pandas as pd


def dataProcess(data,date_start=[], date_end=[]):
    """
    求该机组基于时间的数据完整度
    :param data_7s: 7s数据
    :param date_start: 起始日期,若无,则默认为min(ts);
    :param date_end: 结束日期,若无,则默认为max(ts);
    :return:
    """

    # 处理数据
    columns = ['wfid', 'wtid', 'date_start', 'date_end', 'date_start_real', 'date_end_real', 'hour', 'line', 'data_integrity', 'sample_freq', 'limpow_percent', 'usable_percent']
    result = pd.DataFrame(columns=columns)

    #求行级时间差
    # data = time_diff(data_7s, 'ts', flag=1)

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

    time_diff_value = datetime.strptime(date_end, '%Y-%m-%d') - datetime.strptime(date_start, '%Y-%m-%d')
    hour_total = time_diff_value.total_seconds() / 3600 + 24

    result.loc[0, 'date_start_real'] = data['ts'].min()[0:10]
    result.loc[0, 'date_end_real'] = data['ts'].max()[0:10]
    result.loc[0, 'hour'] = hour_actual
    result.loc[0, 'line'] = len(data)
    result.loc[0, 'data_integrity'] = hour_actual / hour_total
    result.loc[0, 'sample_freq'] = data['ts_diff'].mean()
    result.loc[0, 'limpow_percent'] = data['WTUR_Other_Rn_I16_LimPow'].sum() / len(data)
    result.loc[0, 'usable_percent'] = data['WTUR_State_Rn_I8'].sum() / len(data)
    return (result)


wtid = '632500001'
start_time = '2019-01-01 00:00:00'
end_time = '2019-12-31 00:00:00'
#
# columns = "wfid, wtid, ts, WTUR_Other_Rn_I16_LimPow, WTUR_State_Rn_I8"
# external_condition = "and WTUR_State_Rn_I8 = 1"
# data_7s = prepare_data(wtid, start_time, end_time, columns, external_condition)


time_diff_sql = "select " \
              "wfid,wtid,WTUR_Other_Rn_I16_LimPow, WTUR_State_Rn_I8, " \
              "date_diff('second',ts ,nth_value(ts, no+1) OVER ( ORDER BY no rows BETWEEN unbounded preceding AND unbounded following)) as ts_diff," \
              "ts," \
              "nth_value(ts, no+1) OVER ( ORDER BY no rows BETWEEN unbounded preceding AND unbounded following)  AS third_most_sal " \
              "from (" \
              "select wfid,wtid,WTUR_Other_Rn_I16_LimPow, WTUR_State_Rn_I8," \
              "cast(substr(ts,1,19) as timestamp) ts," \
              "row_number() over(order by ts) no " \
              "from " + table + "where  wtid = '" + wtid + "' and ts >= '" + start_time + "' and ts < '" + end_time + "'" + "' and WTUR_State_Rn_I8 = 1)"

data_7s=aws_helper.execute_query_aws(db, time_diff_sql)

dataProcess(data_7s,'2019-01-01', '2019-12-31')