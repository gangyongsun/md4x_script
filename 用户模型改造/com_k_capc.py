# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019

@author: 33888
"""
"""
功能: 求该机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts, WTUR_WSpd_Ra_F32, WTUR_PwrAt_Ra_F32, WTUR_Temp_Ra_F32；  
                 2) 各风场海拔、空气密度(用于将风速矫正)
输出: 机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
算法：
"""

import pandas as pd
import os

def WindNorm_altitude(altitude,tem,wind,densi):   # 根据海拔和温度将风速标准化
    AirDen = densi
    undernum=1+(1/273.15)*tem
    upnum=1.293*10**(-(altitude/(18400*undernum)))
    airdensity= upnum/undernum
    windnorm = wind*(airdensity/AirDen)**(1/3)
    return(windnorm)  

def compute_com(data_10min):
    # 功能：计算每仓符合度
    # 输入：data_10min——为尚未剔除的10min数据，包含：wfid、wtid、WTUR_WSpd_Ra_F32、WTUR_PwrAt_Ra_F32、windbin、power（担保/设计功率）、flag(0保留1剔除)
    # 输出：每仓符合度
    data_10min = data_10min[data_10min['flag']==0]  # 剔除点
    data_10min = data_10min.drop('flag',axis=1)
    windbin_com = data_10min.groupby(['wfid','wtid','windbin']).mean()   # 分仓求平均
    windbin_com['count'] = data_10min.groupby(['wfid','wtid','windbin'])['WTUR_WSpd_Ra_F32'].count()
    windbin_com = windbin_com.reset_index()
    windbin_com = windbin_com.dropna()               # 去掉不满足条件的风速仓
    windbin_com = windbin_com[windbin_com['count']>=3]          # 去掉点数小于3的风速仓
    windbin_com['comformity'] = windbin_com['WTUR_PwrAt_Ra_F32']/windbin_com['power']
    return(windbin_com)
    
def compute_k(data_10min):
    # 功能：计算K值
    # 输入：data_10min——为尚未剔除的10min数据，包含：wfid、wtid、WTUR_WSpd_Ra_F32、WTUR_PwrAt_Ra_F32、windbin、power（担保/设计功率）、flag(0保留1剔除)
    # 输出：K值
    # 算风频
    windbin_fre = data_10min.groupby(['wfid','wtid','windbin'])['WTUR_WSpd_Ra_F32'].count()   # 分仓求平均
    windbin_fre = pd.DataFrame(windbin_fre)
    windbin_fre.columns = ['num']
    windbin_fre = windbin_fre.reset_index()
    # 算功率曲线
    data_10min_del = data_10min[data_10min['flag']==0]  # 剔除点
    data_10min_del = data_10min_del.drop('flag',axis=1)
    windbin_com = data_10min_del.groupby(['wfid','wtid','windbin']).mean()   # 分仓求平均
    windbin_com['count'] = data_10min_del.groupby(['wfid','wtid','windbin'])['WTUR_WSpd_Ra_F32'].count()
    windbin_com = windbin_com.reset_index()
    windbin_com = windbin_com.dropna()               # 去掉不满足条件的风速仓
    windbin_com = windbin_com[windbin_com['count']>=3]          # 去掉点数小于3的风速仓
    windbin_com = windbin_com.drop('count',axis=1)
    # 计算k
    windbin_com = pd.merge(windbin_com,windbin_fre,how='left',on=['wfid','wtid','windbin'])
    windbin_com['actual_pow_sum'] = windbin_com['WTUR_PwrAt_Ra_F32']*windbin_com['num']
    windbin_com['design_pow_sum'] = windbin_com['power']*windbin_com['num']
    k = windbin_com['actual_pow_sum'].sum()/windbin_com['design_pow_sum'].sum()
    return(k)

def compute_capc(windbin_com):
    # 功能：计算capc
    # 输入：df——每仓符合度
    # 输出：capc
    df = windbin_com.copy()
    df['wind_3'] = df['WTUR_WSpd_Ra_F32']**3
    df['wind_3_com'] = df['wind_3']*df['comformity']
    capc = df['wind_3_com'].sum()/df['wind_3'].sum()
    return(capc) 
 
def mainProcess(data,result_dir,gua_pwr_i):
    # 功能：求该机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
    # 输入：data——7s数据；result_dir——输出路径；gua_pwr_i——担保/设计曲线
    # 输出：结果已保存至result_dir路径，并输出result
    # 数据处理
    # 7s转10min
    data['ts_2'] = data['ts'].str[0:10] + ' ' + data['ts'].str[11:15] + '0:00'
    data_10min = data.groupby(['wfid','wtid','ts_2']).mean()      # 7s转10Min
    data_10min['count'] = data.groupby(['wfid','wtid','ts_2'])['WTUR_WSpd_Ra_F32'].count()
    data_10min['flag'] = 1   # 数据是否剔除，0不剔除，1剔除
    data_10min.loc[(data_10min['WTUR_State_Rn_I8']>0.9) & (data_10min['count']>30),'flag'] = 0
    data_10min = data_10min.drop(['WTUR_State_Rn_I8','count'],axis=1)
    data_10min['windbin'] = round(data_10min['WTUR_WSpd_Ra_F32']/0.5 + 0.00000001)*0.5
    data_10min = data_10min.reset_index()
    data_10min = pd.merge(data_10min,gua_pwr_i,how='left',on=['wfid','wtid','windbin'])
    
    windbin_com = compute_com(data_10min)
    k = compute_k(data_10min)
    capc = compute_capc(windbin_com)
    com_k_capc = windbin_com.groupby(['wfid','wtid'])['comformity'].mean()   
    com_k_capc = pd.DataFrame(com_k_capc)
    com_k_capc = com_k_capc.reset_index()
    com_k_capc['k_value'] = k
    com_k_capc['capc'] = capc
    
    windbin_com.to_csv(result_dir + '/' + str(data.loc[0,'wtid']) + '_4_1_com_windbin.csv', index=False)
    com_k_capc.to_csv(result_dir + '/' + str(data.loc[0,'wtid']) + '_4_1_com_k_capc.csv', index=False)
    
    return() 

def dataProcess(data,result_dir,gua_pwr,wtid_info):
    # 功能：求该机组的各仓符合度、平均符合度、K值、功率曲线一致度（CAPC）
    # 输入：data——7s数据；result_dir——输出路径；gua_pwr——担保/设计曲线；wtid_info——海拔、空气密度
    # 输出：结果已保存至result_dir路径，并输出result
    # 数据准备
    data = data[['wfid','wtid','ts','WTUR_WSpd_Ra_F32','WTUR_PwrAt_Ra_F32','WTUR_Temp_Ra_F32','WTUR_State_Rn_I8']]
    wtid = data.loc[0,'wtid']
    # 取出对应机组的设计/担保曲线
    gua_pwr_i = gua_pwr[gua_pwr['wtid'] == wtid]
    gua_pwr_i = gua_pwr_i[['wfid','wtid','windbin','power','density']]
    gua_pwr_i = gua_pwr_i[gua_pwr_i['power'] !=0]   # 防止搜集担保曲线的时候出现功率为0的情况
    gua_pwr_i = gua_pwr_i.reset_index(drop=True)
    if len(gua_pwr_i) == 0:
        print('wtid does not exist in gua_pwr!')
    density = gua_pwr_i.loc[0,'density']
    # wtid_info表
    wtid_info_i = wtid_info[wtid_info['wtid'] == wtid]
    wtid_info_i = wtid_info_i.reset_index(drop=True) 
    if len(wtid_info_i) == 0:
        print('wtid does not exist in wtid_info!')
    altitude = wtid_info_i.loc[0,'altitude']
    data['WTUR_WSpd_Ra_F32'] = WindNorm_altitude(altitude,data['WTUR_Temp_Ra_F32'],data['WTUR_WSpd_Ra_F32'],density)  # 风速折到density下  
    data = data.drop('WTUR_Temp_Ra_F32',axis=1) 
    
    mainProcess(data,result_dir,gua_pwr_i)       
    return()
    


if __name__ == '__main__':
    pdir = r'D:\file\help_analysis\控制性能评估\2020年\03_响水和青海共和\配置信息'
    result_dir = 'D:/file/help_analysis/控制性能评估/program/result'
    data = pd.read_csv(os.path.join(pdir,'data_320923009.csv'), sep=',') 

    gua_pwr = pd.read_csv(os.path.join(pdir,'gua_pwr.csv'), sep=',')
    wtid_info = pd.read_csv(os.path.join(pdir,'wtid_info.csv'), sep=',')

    dataProcess(data,result_dir,gua_pwr,wtid_info)







    



























