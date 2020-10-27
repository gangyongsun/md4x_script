# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019
@author: 33888

Updated on Sun Sep  27 15:11:19 2020
@author: 50508

功能: 求该机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WTUR_Temp_Ra_F32；  
                 2) 各风场海拔、空气密度(用于将风速矫正)
输出: 机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
算法：
"""

from common.db_util import prepare_data

from common.common_util import wind_norm_altitude
from common.common_util import compute_com
from common.common_util import compute_capc
from common.common_util import compute_k

from config.property import input_dir
from config.property import result_dir
from config.property import com_k_cacp_result

import pandas as pd


def main_process(data_7s, gua_pwr_i):
    """
    求该机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
    :param data_7s: 7s数据
    :param gua_pwr_i: 担保/设计曲线
    :return: 结果已保存至result_dir路径，并输出result
    """

    # 7s转10min
    # data['ts_2'] = data['ts'].str[0:10] + ' ' + data['ts'].str[11:15] + '0:00'
    data_10min = data_7s.groupby(['wfid', 'wtid', 'ts_2']).mean()  # 7s转10Min

    data_10min['count'] = data_7s.groupby(['wfid', 'wtid', 'ts_2'])['WTUR_WSpd_Ra_F32'].count()
    data_10min['flag'] = 1  # 数据是否剔除，0不剔除，1剔除
    data_10min.loc[(data_10min['WTUR_State_Rn_I8'] > 0.9) & (data_10min['count'] > 30), 'flag'] = 0

    data_10min = data_10min.drop(['WTUR_State_Rn_I8', 'count'], axis=1)
    data_10min['windbin'] = round(data_10min['WTUR_WSpd_Ra_F32'] / 0.5 + 0.00000001) * 0.5
    data_10min = data_10min.reset_index()
    data_10min = pd.merge(data_10min, gua_pwr_i, how='left', on=['wfid', 'wtid', 'windbin'])

    windbin_com = compute_com(data_10min)
    k = compute_k(data_10min)
    capc = compute_capc(windbin_com)
    com_k_capc = windbin_com.groupby(['wfid', 'wtid'])['comformity'].mean()
    com_k_capc = pd.DataFrame(com_k_capc)
    com_k_capc = com_k_capc.reset_index()
    com_k_capc['k_value'] = k
    com_k_capc['capc'] = capc

    windbin_com.to_csv(result_dir + com_k_cacp_result + str(data_7s.loc[0, 'wtid']) + '_4_1_com_windbin.csv', index=False)
    com_k_capc.to_csv(result_dir + com_k_cacp_result + str(data_7s.loc[0, 'wtid']) + '_4_1_com_k_capc.csv', index=False)


def data_process(data_7s, gua_pwr, wtid_info):
    """
    求该机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
    :param data_7s: 7s数据
    :param gua_pwr: 担保/设计曲线
    :param wtid_info: 海拔、空气密度
    :return:
    """

    wtid = data_7s.loc[0, 'wtid']

    # 取出对应机组的设计/担保曲线
    gua_pwr_i = gua_pwr[gua_pwr['wtid'] == wtid]
    gua_pwr_i = gua_pwr_i[['wfid', 'wtid', 'windbin', 'power', 'density']]

    # 防止搜集担保曲线的时候出现功率为0的情况
    gua_pwr_i = gua_pwr_i[gua_pwr_i['power'] != 0]
    gua_pwr_i = gua_pwr_i.reset_index(drop=True)

    if len(gua_pwr_i) == 0:
        print('wtid does not exist in gua_pwr!')

    density = gua_pwr_i.loc[0, 'density']

    # wtid_info表
    wtid_info_i = wtid_info[wtid_info['wtid'] == wtid]
    wtid_info_i = wtid_info_i.reset_index(drop=True)

    if len(wtid_info_i) == 0:
        print('wtid does not exist in wtid_info!')

    altitude = wtid_info_i.loc[0, 'altitude']

    data_7s['WTUR_WSpd_Ra_F32'] = wind_norm_altitude(altitude, data_7s['WTUR_Temp_Ra_F32'], data_7s['WTUR_WSpd_Ra_F32'], density)  # 风速折到density下
    data_7s = data_7s.drop('WTUR_Temp_Ra_F32', axis=1)

    main_process(data_7s, gua_pwr_i)


#准备7s数据
wtid = '632500001'
start_time = '2019-01-01 00:00:00'
end_time = '2019-12-31 00:00:00'

columns = "wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WTUR_Temp_Ra_F32, WTUR_State_Rn_I8, concat(substring(ts,1,15),'0:00') AS ts_2"
external_condition = "and WTUR_State_Rn_I8 = 1"
data_7s = prepare_data(wtid, start_time, end_time, columns, external_condition)

#读取文件
gua_pwr = pd.read_csv(input_dir + 'gua_pwr.csv', sep=',')
wtid_info = pd.read_csv(input_dir + 'wtid_info.csv', sep=',')

#执行逻辑
data_process(data_7s, gua_pwr, wtid_info)