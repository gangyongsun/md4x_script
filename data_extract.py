# *_*coding:utf-8 *_*

from common.DBUtil import exec_sql
from common.ComputeUtil import time_diff
from config.property import db
from config.property import table

from datetime import datetime

import pandas as pd
import time


def dataProcess():
    # 1.where条件
    where_condition = "where wtid in ('632500001','632500002','632500003','632500004','632500005') and ts >= '2019-01-01 00:00:00' and ts < '2019-12-31 00:00:00'"

    # 2.选择列
    #result_column = "wfid,wtid,ts,WTUR_Other_Rn_I16_LimPow,WTUR_State_Rn_I8"
    result_column = "wfid,wtid,ts,WTUR_WSpd_Ra_F32,WTUR_WSpd_Ra_F32_2,WTUR_PwrAt_Ra_F32,WGEN_Spd_Ra_F32,WCNV_Other_Ra_F32_TorqueReference,WCNV_Other_Ra_F32_Torque,WTUR_Acce_Ra_F32_x,WTUR_Acce_Ra_F32_y,WTPS_Ang_Ra_F32_blade1,WTPS_Ang_Ra_F32_blade2,WTPS_Ang_Ra_F32_blade3,WTPS_Spd_Ra_F32_blade1,WTUR_Wdir_Ra_F32,WYAW_Wdir_Ra_F32,WYAW_Spd_Ra_F32_Yaw,WYAW_Posi_Ra_F32,WTUR_Temp_Ra_F32,WTUR_Other_Rn_I16_LimPow,WTUR_State_Rn_I8,WTUR_Other_Wn_I16_StopModeWord,WTUR_Flt_Ri_I32_main,WTUR_TurSt_Rs_S,WTUR_Other_Rn_U16_GlobalStopLevel"

    # 3.分析数据准备
    sql = "select " + result_column + " from {0} " + where_condition
    sql = sql.format(table)

    # 7s数据
    data = exec_sql(db, sql)
    return (data)

def integrityProcess(date_start,date_end,data):
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


def exec_summary():
    start_time = time.time()
    data = dataProcess()
    end_time = time.time()

    integrityProcess('2019-01-1', '2019-12-31', data)
    end_time_again = time.time()

    exec_time = end_time - start_time
    exec_time_again = end_time_again - end_time

    print("数据抽取时间：%.2f s，完整度计算时间：%.2f s" % (exec_time, exec_time_again))


for i in range(5):
    exec_summary()
