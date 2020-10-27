# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019

@author: 33888
"""
"""
功能: 求该机组的特性曲线和特性曲线散点图
输入: 涉及数据为: 1) 7s数据变量
                 2) 各风场海拔、空气密度(用于将风速矫正)
输出: character_curve.csv（n*11）
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def WindNorm_altitude(altitude, temperature, wind, density):  # 根据海拔和温度将风速标准化
    # undernum = 1 + (1 / 273.15) * temperature
    # upnum = 1.293 * 10 ** (-(altitude / (18400 * undernum)))
    # airdensity = upnum / undernum
    # windnorm = wind * (airdensity / density) ** (1 / 3)

    windnorm = wind * (1.293 * 10 ** (-(altitude / (18400 * (1 + (1 / 273.15) * temperature)))) / (1 + (1 / 273.15) * temperature) / density) ** (1 / 3)
    return(windnorm)

def plot(data,result,result_2,result_dir):
    # 功能：绘图：7s散点+实际曲线，10min散点+实际曲线，已剔除异常值
    # 输入：data——7s数据；result——10Min数据；result_2——拟合曲线
    data_1 = data[data['WTUR_State_Rn_I8']==1]
    
    # 1 风速-功率
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WTUR_PwrAt_Ra_F32'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WTUR_PwrAt_Ra_F32'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WTUR_PwrAt_Ra_F32'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("power [kW]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_1_win_pow_7s.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    
    plt.figure()
    plt.scatter(result['WTUR_WSpd_Ra_F32'], result['WTUR_PwrAt_Ra_F32'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WTUR_PwrAt_Ra_F32'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WTUR_PwrAt_Ra_F32'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("power [kW]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_1_win_pow_10min.png',dpi=300,bbox_inches = 'tight')
    plt.close() 
    
    # 2 风速-转速
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WGEN_Spd_Ra_F32'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WGEN_Spd_Ra_F32'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WGEN_Spd_Ra_F32'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("generator speed [rpm]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_2_win_gen_7s.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    
    plt.figure()
    plt.scatter(result['WTUR_WSpd_Ra_F32'], result['WGEN_Spd_Ra_F32'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WGEN_Spd_Ra_F32'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WGEN_Spd_Ra_F32'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("generator speed [rpm]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_2_win_gen_10min.png',dpi=300,bbox_inches = 'tight')
    plt.close() 
    
    # 3 风速-扭矩
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_3_win_tor_7s.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    
    plt.figure()
    plt.scatter(result['WTUR_WSpd_Ra_F32'], result['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_3_win_tor_10min.png',dpi=300,bbox_inches = 'tight')
    plt.close() 
    
     # 4 转速-扭矩
    plt.figure()
    plt.scatter(data_1['WGEN_Spd_Ra_F32'], data_1['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WGEN_Spd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], color = '#E15759')
    plt.scatter(result_2['WGEN_Spd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#E15759')
    plt.xlabel("generator speed [rpm]",fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_4_gen_tor_7s.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    
    plt.figure()
    plt.scatter(result['WGEN_Spd_Ra_F32'], result['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WGEN_Spd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], color = '#E15759')
    plt.scatter(result_2['WGEN_Spd_Ra_F32'], result_2['WCNV_Other_Ra_F32_TorqueReference'], s = 0.5, color = '#E15759')
    plt.xlabel("generator speed [rpm]",fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_4_gen_tor_10min.png',dpi=300,bbox_inches = 'tight')
    plt.close() 
    
    # 5 风速-桨距角
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WTPS_Ang_Ra_F32_blade1'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['WTUR_WSpd_Ra_F32'], result_2['WTPS_Ang_Ra_F32_blade1'], color = '#E15759')
    plt.scatter(result_2['WTUR_WSpd_Ra_F32'], result_2['WTPS_Ang_Ra_F32_blade1'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("pitch angle [deg]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_5_win_pit_7s.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    
    plt.figure()
    plt.scatter(result['WTUR_WSpd_Ra_F32'], result['WTPS_Ang_Ra_F32_blade1'], s = 0.5, color = '#4E79A7')
    plt.plot(result_2['windbin'], result_2['WTPS_Ang_Ra_F32_blade1'], color = '#E15759')
    plt.scatter(result_2['windbin'], result_2['WTPS_Ang_Ra_F32_blade1'], s = 0.5, color = '#E15759')
    plt.xlabel("wind [m/s]",fontproperties="STXihei")
    plt.ylabel("pitch angle [deg]",fontproperties="STXihei")
    plt.grid()
    plt.show()
    plt.savefig(result_dir + '/' + str(data.loc[0,'wtid']) + '_3_1_5_win_pit_10min.png',dpi=300,bbox_inches = 'tight')
    plt.close()
    
    return()

def main_process(data_7s, result_dir):
    # 功能：求该机组的特性曲线和特性曲线散点图
    # 输入：data——7s数据；result_dir——输出路径
    # 输出：结果已保存至result_dir路径，并输出result
    # 数据处理
    
    data_7s['ts_2'] = data_7s['ts'].str[0:10] + ' ' + data_7s['ts'].str[11:15] + '0:00'

    data_10min = data_7s.groupby(['wfid', 'wtid', 'ts_2']).mean()      # 7s转10Min

    data_10min['count'] = data_7s.groupby(['wfid', 'wtid', 'ts_2'])['WTUR_WSpd_Ra_F32'].count()

    data_10min = data_10min[(data_10min['WTUR_State_Rn_I8']>0.9) & (data_10min['count']>30)]

    data_10min['windbin'] = round(data_10min['WTUR_WSpd_Ra_F32']/0.5 + 0.00000001)*0.5
    data_10min = data_10min.reset_index()

    result_2 = data_10min.groupby(['wfid','wtid','windbin']).mean()   # 分仓求平均
    result_2 = result_2.drop(['WTUR_State_Rn_I8','count'],axis=1)
    result_2['count'] = data_10min.groupby(['wfid','wtid','windbin'])['WTUR_WSpd_Ra_F32'].count()
    result_2 = result_2.reset_index()
    result_2.to_csv(result_dir + '/' + str(data_7s.loc[0, 'wtid']) + '_3_1_character_curve.csv', index=False)

    plot(data_7s, data_10min, result_2, result_dir)
    
    return() 

def dataProcess(data,result_dir,wind_is_correct=0,wtid_info=[]):
    # 功能：求该机组的特性曲线和特性曲线散点图
    # 输入：data——7s数据；result_dir——输出路径; 若wind_is_correct=1，则需输入wtid_info,否则只需输入data即可
    # 输出：结果已保存至result_dir路径，并输出result
    # 数据准备
    if wind_is_correct == 0:
        data = data[['wfid','wtid','ts','WTUR_WSpd_Ra_F32','WTUR_PwrAt_Ra_F32','WGEN_Spd_Ra_F32','WCNV_Other_Ra_F32_TorqueReference','WTPS_Ang_Ra_F32_blade1','WTUR_State_Rn_I8']]
    elif wind_is_correct == 1:
        data = data[['wfid','wtid','ts','WTUR_WSpd_Ra_F32','WTUR_PwrAt_Ra_F32','WGEN_Spd_Ra_F32','WCNV_Other_Ra_F32_TorqueReference','WTPS_Ang_Ra_F32_blade1','WTUR_State_Rn_I8','WTUR_Temp_Ra_F32']]
        wtid = data.loc[0,'wtid']
        # wtid_info表
        wtid_info_i = wtid_info[wtid_info['wtid'] == wtid]
        wtid_info_i = wtid_info_i.reset_index()
        wtid_info_i = wtid_info_i.drop('index',axis=1)
        altitude = wtid_info_i.loc[0,'altitude']
        density = wtid_info_i.loc[0,'density']
        data['WTUR_WSpd_Ra_F32'] = WindNorm_altitude(altitude,data['WTUR_Temp_Ra_F32'],data['WTUR_WSpd_Ra_F32'],density)  # 风速折到density下  
       
    main_process(data,result_dir)       
    return()
    


if __name__ == '__main__':
    pdir = '/Users/alvin/Downloads/'
    result_dir = '/Users/alvin/Downloads/result'
    data = pd.read_csv(os.path.join(pdir,'character_curve_7s.csv'), sep=',')
    dataProcess(data,result_dir)







    

