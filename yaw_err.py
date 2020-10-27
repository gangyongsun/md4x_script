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

from common.common_util import yawerrorcal
from common.db_util import exec_sql
from config.property import db
from config.property import table

def main_process(data):
    # 功能：求该机组的对风偏差
    # 输入：data——7s数据

    # 数据处理
    wfid = data['wfid'].iloc[0]
    wtid = data['wtid'].iloc[0]
    # 这一步在SQL完成
    # data = data.loc[(data['WTUR_State_Rn_I8'] == 1) & (data['WTPS_Ang_Ra_F32_blade1'] < 2),]
    yawerrorcal(data, wfid, wtid)

def dataProcess():
    # 功能：求该机组的对风偏差

    wtid_data = '632500001'
    start_time = '2019-01-01 00:00:00'
    end_time = '2019-12-31 00:00:00'

    # 基本where条件
    condition_where = " where wtid = '" + wtid_data + "' and ts >= '" + start_time + "' and ts < '" + end_time  + "' and WTUR_State_Rn_I8 = 1 and WTPS_Ang_Ra_F32_blade1 < 2 "
    # condition_where = " where wtid >= '632500001' and wtid<='632500020' and ts >= '" + start_time + "' and ts < '" + end_time + "' and WTUR_State_Rn_I8=1 and WTPS_Ang_Ra_F32_blade1 < 2 "

    # 2.选择列
    result_column = "wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WYAW_Wdir_Ra_F32, WTUR_State_Rn_I8, WTPS_Ang_Ra_F32_blade1"

    # 3.SQL
    sql = "select " + result_column + " from {0} " + condition_where
    sql = sql.format(table)
    # 执行查询获取7s数据
    data = exec_sql(db, sql)
    main_process(data)

dataProcess()