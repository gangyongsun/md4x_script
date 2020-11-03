# *_*coding:utf-8 *_*
"""
Created on Mon Aug  5 12:15:29 2019

@author: 33888
"""
"""
功能: 求该机组基于时间的数据完整度
输入: 涉及数据为: 1) 7s数据变量：wfid, wtid, ts；  
输出: data_integrity.csv（1*5） 
"""

import pandas as pd
import os
import datetime
    
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

def dataProcess(data,result_dir,date_start=[],date_end=[]):
    # 功能：求该机组基于时间的数据完整度
    # 输入：data——7s数据；result_dir——输出路径；date_start——起始日期，如’2019-01-01’，若无，则默认为min(ts)；date_end——结束日期，如’2019-05-31’，若无，则默认为max(ts)
    # 输出：结果已保存至result_dir路径，并输出result
    # 数据准备
    data = data[['wfid','wtid','ts','WTUR_Other_Rn_I16_LimPow','WTUR_State_Rn_I8']]
    # 处理数据
    result = pd.DataFrame(columns = ['wfid','wtid','date_start','date_end','date_start_real','date_end_real','hour','line','data_integrity','sample_freq','limpow_percent','usable_percent'])
    data = time_diff(data,'ts',flag=1)
    hour_actual = data['ts_diff'].sum()/3600
    
    result.loc[0,'wfid'] = data.loc[0,'wfid']
    result.loc[0,'wtid'] = data.loc[0,'wtid']
    
    if len(date_start) != 0:
        result.loc[0,'date_start'] = date_start
    else:
        date_start = data['ts'].min()[0:10]
    if len(date_end) != 0:
        result.loc[0,'date_end'] = date_end
    else:
        date_end = data['ts'].max()[0:10]
    
    
    a = datetime.datetime.strptime(date_end, '%Y-%m-%d') - datetime.datetime.strptime(date_start, '%Y-%m-%d')
    hour_total = a.total_seconds()/3600 + 24 
    
    result.loc[0,'date_start_real'] = data['ts'].min()[0:10]
    result.loc[0,'date_end_real'] = data['ts'].max()[0:10]
    result.loc[0,'hour'] = hour_actual
    result.loc[0,'line'] = len(data)
    result.loc[0,'data_integrity'] = hour_actual/hour_total
    result.loc[0,'sample_freq'] = data['ts_diff'].mean()
    result.loc[0,'limpow_percent'] = data['WTUR_Other_Rn_I16_LimPow'].sum()/len(data)
    result.loc[0,'usable_percent'] = data['WTUR_State_Rn_I8'].sum()/len(data)
    result.to_csv(result_dir + '/' + str(data.loc[0,'wtid']) + '_1_1_data_integrity.csv', index=False)
    return(result)
    


if __name__ == '__main__':
    pdir = 'D:/file/help_analysis/zhangxinli/program/data_example'
    result_dir = 'D:/file/help_analysis/控制性能评估/program/result'
    data = pd.read_csv(os.path.join(pdir,'part-00179-0f3ccc61-0fbc-43b2-8baa-74b3dab46258.c000_wt.csv'), sep=',') 
    result = dataProcess(data,result_dir,'2019-01-01','2019-05-01')







    

