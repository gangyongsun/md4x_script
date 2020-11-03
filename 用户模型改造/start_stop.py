# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019

@author: 33888
"""
"""
功能：此程序用于启停机时长和次数统计
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts, WTUR_TurSt_Rs_S,WTUR_WSpd_Ra_F32等; 
输出: start_stop: 启停机时长统计：wfid, wtid, ts, 起/停机, 时长(s)
"""

import pandas as pd
import numpy as np
import os
import datetime
import math
import matplotlib.pyplot as plt

def WindNorm_altitude(altitude,tem,wind,densi):   # 根据海拔和温度将风速标准化
    AirDen = densi
    undernum=1+(1/273.15)*tem
    upnum=1.293*10**(-(altitude/(18400*undernum)))
    airdensity= upnum/undernum
    windnorm = wind*(airdensity/AirDen)**(1/3)
    return(windnorm)  

def time_diff(data,var,flag=0):
    # 功能：此函数用于计算行与行之间秒级的时间差
    # 输入：data数据集，var为指定的时间变量名(eg: ts/WTUR_Tm_Rw_Dt,可字符串可时间类型)
    #       flag=0，异常时间差不做任何处理；flag=1，超过(mean*2)的时间差用round(mean)代替
    # 输出：在原数据集的最后一列加一列*_diff, 输出结果已按时间排序，索引已重置，第一行的空值用第二个值代替
    var_output = var + '_diff'
    if isinstance(data.loc[data.index[0],var],str):  # 判断是否为字符串
        data['ts_1'] = pd.to_datetime(data[var], format = '%Y-%m-%d %H:%M:%S')
    else:
        data['ts_1'] = data[var] 
    data = data.sort_values('ts_1')    # 对时间排序
    data = data.reset_index()
    data = data.drop('index',axis=1)    
    data[var_output] = data['ts_1'].diff()
    data[var_output] = [i.total_seconds() for i in data[var_output]]
    data.loc[0,var_output] = data.loc[1,var_output]   # 用第二个值代替第一个值
    
    if flag == 1:
        ts_mean = data[var_output].mean()
        data.loc[data[var_output]>(ts_mean*2),var_output] = round(ts_mean)
    
    data = data.drop('ts_1', axis=1)
    return(data)   
    
def state_recognize(df,var_name):          
    # 功能：在输入的数据集上加一列：var_name_slice(每次状态切换的不重复标记) 
    # 输入：数据集df，需要做不重复标记的变量名var_name
    # 输出：df加一列var_name_slice
    # 注：若var_name那一列是相同的值，则var_name_slice全为1
    var_slice = var_name + '_slice'
    var_diff = var_name + '_diff_x'
    if len(df[var_name].unique()) == 1:  # 只有一种状态
        df[var_slice] = 1
    else:
        #计算状态差
        df[var_diff] = df[var_name].diff()
        df.loc[0,var_diff] = 0

        #加编号列：ID_1
        a = np.linspace(0,len(df)-1,len(df))
        df['ID_1'] = a.reshape(len(df),1)

        #取有状态变化的ID_1列
        a = df.loc[df[var_diff] != 0,'ID_1']
        a = a.reset_index()

        #删除index
        a = a.drop('index',axis=1)

        df[var_slice] = 0

        df.loc[0:int(a.loc[0]-1),var_slice] = 1

        for i in range(0,len(a)):
            if i == (len(a)-1):
                df.loc[int(a.loc[i]):(len(df)-1),var_slice] = i+2
            else:
                df.loc[int(a.loc[i]):int(a.loc[i+1]-1),var_slice] = i+2
        df = df.drop([var_diff,'ID_1'], axis=1)
    return(df)
    
def start_stop_extract(df,data):
    # 功能：基于df取出起停机的时长、时间范围、平均风速
    # 输入：df——每个风机状态一行统计结果，包含时间范围、时长、是否连续；data——7s数据，包含时间、风速; flag——若为1，则输出状态3和4时的变桨速率和扭矩反馈；若为0，则不输出
    # 输出：re——起停机的时长、时间范围、平均风速；spdblade_tor——风机状态为3和4时的变桨速率和扭矩反馈
    # 起机提取：3-4-5，统计3和4的时长以及平均风速
    re_1 = pd.DataFrame()
    for i in range(0, (len(df)-2)):
        if (df.loc[i,'WTUR_TurSt_Rs_S'] == 3) & (df.loc[(i+1),'WTUR_TurSt_Rs_S'] == 4) & (df.loc[(i+2),'WTUR_TurSt_Rs_S'] == 5) & (df.loc[[i,i+1,i+2],'is_discontinue'].sum() == 0):
            ts_start = df.loc[i,'ts_start']
            ts_end_1 = df.loc[i,'ts_end']
            ts_end_2 = df.loc[(i+1),'ts_end']
            re_1_i = df.loc[[i],:] 
            re_1_i = re_1_i[['wfid','wtid']]
            re_1_i['ts_start'] = ts_start
            re_1_i['ts_end'] = ts_end_2
            re_1_i['seconds'] = df.loc[i,'seconds'] + df.loc[(i+1),'seconds']
            re_1_i['seconds_3'] = df.loc[i,'seconds']
            re_1_i['seconds_3_1'] = data.loc[(data['ts']>=ts_start) & (data['ts']<=ts_end_1) & (data['WTPS_Ang_Ra_F32_blade1']>55),'ts_diff'].sum()
            re_1_i['seconds_3_2'] = re_1_i['seconds_3'] - re_1_i['seconds_3_1']
            re_1_i['seconds_4'] = df.loc[(i+1),'seconds']
            re_1_i['wind_mean'] = data.loc[(data['ts']>=ts_start) & (data['ts']<=ts_end_2),'WTUR_WSpd_Ra_F32'].mean()
            re_1_i['wind_mean_3_1'] = data.loc[(data['ts']>=ts_start) & (data['ts']<=ts_end_1) & (data['WTPS_Ang_Ra_F32_blade1']>55),'WTUR_WSpd_Ra_F32'].mean()
            re_1_i['wind_mean_4'] = data.loc[(data['ts']>=ts_end_1) & (data['ts']<=ts_end_2),'WTUR_WSpd_Ra_F32'].mean()
            re_1_i['state'] = 'start'
            re_1 = re_1.append(re_1_i)
    # 停机提取：5-1，统计1的时长以及平均风速
    re_2 = pd.DataFrame()
    for i in range(0, (len(df)-1)):
        if (df.loc[i,'WTUR_TurSt_Rs_S'] == 5) & (df.loc[(i+1),'WTUR_TurSt_Rs_S'] == 1) & (df.loc[[i,i+1],'is_discontinue'].sum() == 0):
            ts_start = df.loc[(i+1),'ts_start']
            ts_end = df.loc[(i+1),'ts_end']
            re_2_i = df.loc[[i+1],:] 
            re_2_i['wind_mean'] = data.loc[(data['ts']>=ts_start) & (data['ts']<=ts_end),'WTUR_WSpd_Ra_F32'].mean()
            re_2_i['state'] = 'stop'
            re_2_i = re_2_i[['wfid','wtid','ts_start','ts_end','seconds','wind_mean','state']] 
            re_2 = re_2.append(re_2_i)
    
    re = pd.concat([re_1, re_2], axis = 0) 
    re = re.sort_values('ts_start')
    re = re.reset_index()
    re = re.drop('index',axis=1)
    re = re[['wfid','wtid','ts_start','ts_end','seconds','seconds_3','seconds_3_1','seconds_3_2','seconds_4','wind_mean','wind_mean_3_1','wind_mean_4','state']]
    return(re)
    
def start_2h_count(start_stop,data,result_dir):
    # 功能：基于start_stop将时间按两小时切割，计算起机次数  
    # 输入：start_stop——起停机时长、时间范围、平均风速；data——原始7s数据
    # 输出：start_2h
    # 1. 对start_stop的时间进行划分，统计次数
    start_stop = start_stop[start_stop['state']=='start']
    start_stop['date'] = start_stop['ts_start'].str[0:10]
    start_stop['ts_start'] = pd.to_datetime(start_stop['ts_start'], format = '%Y-%m-%d %H:%M:%S')
    start_stop['hour'] = [i.hour for i in start_stop['ts_start']]    # 取出小时
    start_stop['ID'] = [math.floor(i/2)*2 for i in start_stop['hour']]   # 对小时做变换
    result_1 =start_stop.groupby(['wfid','wtid','date','ID'])['hour'].count()
    result_1 = pd.DataFrame(result_1)
    result_1.columns = ['count']
    result_1 = result_1.reset_index()
    # 2. 对data的时间进行划分，统计平均风速
    data['date'] = data['ts'].str[0:10]
    data['ts'] = pd.to_datetime(data['ts'], format = '%Y-%m-%d %H:%M:%S')
    data['hour'] = [i.hour for i in data['ts']]    # 取出小时
    data['ID'] = [math.floor(i/2)*2 for i in data['hour']]   # 对小时做变换
    result_2 =data.groupby(['wfid','wtid','date','ID'])['WTUR_WSpd_Ra_F32'].mean()
    result_2 = pd.DataFrame(result_2)
    result_2.columns = ['wind_mean']
    result_2 = result_2.reset_index()
 
    re = pd.merge(result_1,result_2,how='right',on = ['wfid','wtid','date','ID'])
    re = re.fillna(0)
    re['date'] = pd.to_datetime(re['date'], format = '%Y-%m-%d')
    re['ts_start'] = [datetime.datetime(re.loc[i,'date'].year,re.loc[i,'date'].month,re.loc[i,'date'].day,int(re.loc[i,'ID'])).strftime('%Y-%m-%d %H:%M:%S') for i in re.index]
    re = re[['wfid','wtid','ts_start','count','wind_mean']]
    re = re.sort_values('ts_start')
    re = re.reset_index()
    re = re.drop('index',axis=1)

    return(re)
    
def plot(start_stop,start_2h,data,result_dir):
    # 绘图 
    # 1
    plt.figure()
    plt.scatter(start_2h['wind_mean'], start_2h['count'], s = 6, color = '#4E79A7')
    plt.xlabel("2h wind mean [m/s]",fontproperties="STXihei")
    plt.ylabel("start count",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_4_1_wind2h_count.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    # 2
    start = start_stop[start_stop['state']=='start']
    plt.figure()
    plt.scatter(start['wind_mean'], start['seconds'], s = 6, color = '#4E79A7')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("start duration [s]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_4_1_wind_start_duration.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    # 3
    stop = start_stop[start_stop['state']=='stop']
    plt.figure()
    plt.scatter(stop['wind_mean'], stop['seconds'], s = 6, color = '#4E79A7')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("stop duration [s]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_4_1_wind_stop_duration.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    return()
    
def main_process(data,result_dir,limit):
    # 1. 前期处理：根据风机状态将数据切割，取出时长和时间范围，并判断是否连续
    data = data.sort_values('ts')
    data = data.reset_index(drop = True)
    data = time_diff(data,'ts')       # 加一列：ts_diff，异常值不能用round(mean)代替
    data_1 = state_recognize(data,'WTUR_TurSt_Rs_S')
    result = data_1.groupby(['wfid','wtid','WTUR_TurSt_Rs_S','WTUR_TurSt_Rs_S_slice'])['ts_diff'].sum()
    result = pd.DataFrame(result)
    result['ts_diff_max'] = data_1.groupby(['wfid','wtid','WTUR_TurSt_Rs_S','WTUR_TurSt_Rs_S_slice'])['ts_diff'].max()
    result['ts_start'] = data_1.groupby(['wfid','wtid','WTUR_TurSt_Rs_S','WTUR_TurSt_Rs_S_slice'])['ts'].min()
    result['ts_end'] = data_1.groupby(['wfid','wtid','WTUR_TurSt_Rs_S','WTUR_TurSt_Rs_S_slice'])['ts'].max()
    result = result.reset_index() 
    result['is_discontinue'] = [(1 if i > limit else 0) for i in result['ts_diff_max']]
    result = result.sort_values('WTUR_TurSt_Rs_S_slice')
    result = result.reset_index()
    result = result.drop('index',axis=1)   
    result = result.rename(columns = {'ts_diff':'seconds'})
    # 2. 结果1：基于result统计起停机时长、时间范围、平均风速
    start_stop = start_stop_extract(result,data)   # 基于result取出起停机的时长、时间范围、平均风速
    start_stop.to_csv(result_dir + '/' + str(data.loc[0,'wtid']) + '_5_1_start_stop_slice.csv', index=False)
    # 3. 结果2：基于result统计起停机时长、时间范围、平均风速
    start_stop_sta = start_stop.groupby(['wfid','wtid','state'])['wtid'].count()
    start_stop_sta = pd.DataFrame(start_stop_sta)
    start_stop_sta.columns = ['count']    
    start_stop_sta['seconds_min'] = start_stop.groupby(['wfid','wtid','state'])['seconds'].min()
    start_stop_sta['seconds_max'] = start_stop.groupby(['wfid','wtid','state'])['seconds'].max()
    start_stop_sta['seconds_mean'] = start_stop.groupby(['wfid','wtid','state'])['seconds'].mean()    
    start_stop_sta['seconds_3_1_min'] = start_stop.groupby(['wfid','wtid','state'])['seconds_3_1'].min()
    start_stop_sta['seconds_3_1_max'] = start_stop.groupby(['wfid','wtid','state'])['seconds_3_1'].max()
    start_stop_sta['seconds_3_1_mean'] = start_stop.groupby(['wfid','wtid','state'])['seconds_3_1'].mean()    
    start_stop_sta['seconds_3_2_min'] = start_stop.groupby(['wfid','wtid','state'])['seconds_3_2'].min()
    start_stop_sta['seconds_3_2_max'] = start_stop.groupby(['wfid','wtid','state'])['seconds_3_2'].max()
    start_stop_sta['seconds_3_2_mean'] = start_stop.groupby(['wfid','wtid','state'])['seconds_3_2'].mean()   
    start_stop_sta['seconds_4_min'] = start_stop.groupby(['wfid','wtid','state'])['seconds_4'].min()
    start_stop_sta['seconds_4_max'] = start_stop.groupby(['wfid','wtid','state'])['seconds_4'].max()
    start_stop_sta['seconds_4_mean'] = start_stop.groupby(['wfid','wtid','state'])['seconds_4'].mean()
    start_stop_sta = start_stop_sta.reset_index()
    start_stop_sta.to_csv(result_dir + '/' + str(data.loc[0,'wtid']) + '_5_1_start_stop_count.csv', index=False)    
    # 4. 结果3：基于start_stop将时间按两小时切割，计算起机次数    
    start_2h = start_2h_count(start_stop,data,result_dir)
    start_2h.to_csv(result_dir + '/' + str(data.loc[0,'wtid']) + '_5_1_start_2h.csv', index=False)
    
    #plot(start_stop,start_2h,data,result_dir)
    
    return(start_stop)

def dataProcess(data,result_dir,limit=200,wind_is_correct=0,wtid_info=[]):
    # 功能：用于启停机时长统计
    # 输入：data——7s数据；result_dir——输出路径；limit——当时间间隔超过limit，则认为是间断点，不作统计；若wind_is_correct=1，则需输入wtid_info,否则只需输入data即可
    # 输出：结果已保存至result_dir路径，并输出result
    # 数据准备
    if wind_is_correct == 0:
        data = data[['wfid','wtid','ts','WTUR_WSpd_Ra_F32','WTPS_Ang_Ra_F32_blade1','WTUR_TurSt_Rs_S']]
        print('start_stop var success !')
    elif wind_is_correct == 1:
        data = data[['wfid','wtid','ts','WTUR_WSpd_Ra_F32','WTPS_Ang_Ra_F32_blade1','WTUR_TurSt_Rs_S','WTUR_Temp_Ra_F32']]
        print('start_stop var success !')
        wtid = data.loc[0,'wtid']
        # wtid_info表
        wtid_info_i = wtid_info[wtid_info['wtid'] == wtid]
        wtid_info_i = wtid_info_i.reset_index()
        wtid_info_i = wtid_info_i.drop('index',axis=1)
        altitude = wtid_info_i.loc[0,'altitude']
        density = wtid_info_i.loc[0,'density']
        data['WTUR_WSpd_Ra_F32'] = WindNorm_altitude(altitude,data['WTUR_Temp_Ra_F32'],data['WTUR_WSpd_Ra_F32'],density)  # 风速折到density下  
        data['WTUR_TurSt_Rs_S'] = pd.to_numeric(data['WTUR_TurSt_Rs_S'])
        
    start_stop = main_process(data,result_dir,limit)       
    return(start_stop)
    


if __name__ == '__main__':
    pdir = 'D:/file/help_analysis/zhangxinli/program/data_example'
    result_dir = 'D:/file/help_analysis/控制性能评估/program/result'
    data = pd.read_csv(os.path.join(pdir,'part-00179-0f3ccc61-0fbc-43b2-8baa-74b3dab46258.c000_wt.csv'), sep=',') 
    data = data.loc[0:100000]
    
#    pdir = r'D:\Users\33888\Desktop\kmxhdfs-demo-V4(1)\test\source1'
#    result_dir = r'D:\Users\33888\Desktop\kmxhdfs-demo-V4(1)\test'
#    data = pd.read_csv(os.path.join(pdir,'schema_410201001_201910.csv'), sep=',') 
    
    
#    data = data.loc[0:100000,]
    dataProcess(data,result_dir,limit=200,wind_is_correct=0,wtid_info=[])





    

