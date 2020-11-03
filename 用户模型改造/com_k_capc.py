%python
import pandas as pd
import athena_helper as aws_helper

def compute_k(data_10min_4_compute_com):
    """
    计算K值
    :param data_10min: 按条件处理好的10min数据
    :return: K值
    """
    data_10min_4_compute_com['actual_pow_sum'] = data_10min_4_compute_com['WTUR_PwrAt_Ra_F32'] * data_10min_4_compute_com['count']
    data_10min_4_compute_com['design_pow_sum'] = data_10min_4_compute_com['power'] * data_10min_4_compute_com['count']
    k = data_10min_4_compute_com['actual_pow_sum'].sum() / data_10min_4_compute_com['design_pow_sum'].sum()
    return (k)

def compute_com_process(data_10min_4_compute_com):
    """
    计算每仓符合度
    :param data_10min: 按条件处理好的10min数据
    :return: 每仓符合度
    """
    data_10min_4_compute_com['comformity'] = data_10min_4_compute_com['WTUR_PwrAt_Ra_F32'] / data_10min_4_compute_com['power']
    return (data_10min_4_compute_com)

def compute_capc_process(windbin_com):
    """
    计算capc
    :param windbin_com: 每仓符合度
    :return: capc
    """
    df = windbin_com.copy()
    df['wind_3'] = df['WTUR_WSpd_Ra_F32'] ** 3
    df['wind_3_com'] = df['wind_3'] * df['comformity']
    capc = df['wind_3_com'].sum() / df['wind_3'].sum()
    return (capc)

def com_k_capc_data_process(wfid,wtid_start,wtid_end,date_start,date_end,gua_pwr, wtid_info):
    """
    计算K值CAPC值
    :param wfid: 风场ID
    :param wtid_start: 风机起始ID
    :param wtid_end: 风机结束ID
    :param date_start: 开始日期
    :param date_end: 结束日期
    :param gua_pwr: 配置文件1
    :param wtid_info: 配置文件2
    :return:
    """
    result = pd.DataFrame(columns=['wfid', 'wtid', 'comformity', 'k_value', 'capc'])

    # ==============取出对应机组的设计/担保曲线:start==============
    gua_pwr_i = gua_pwr[gua_pwr['wfid'] == wfid]
    gua_pwr_i = gua_pwr_i[['wfid', 'wtid', 'windbin', 'power', 'density']]

    # 防止搜集担保曲线的时候出现功率为0的情况
    gua_pwr_i = gua_pwr_i[gua_pwr_i['power'] != 0]
    gua_pwr_i = gua_pwr_i.reset_index(drop=True)

    if len(gua_pwr_i) == 0:
        print('wtid does not exist in gua_pwr!')

    density = gua_pwr_i.loc[0, 'density']
    # ==============取出对应机组的设计/担保曲线:end==============

    # =============wtid_info表:start =============
    wtid_info_i = wtid_info[wtid_info['wfid'] == wfid]
    wtid_info_i = wtid_info_i.reset_index(drop=True)

    if len(wtid_info_i) == 0:
        print('wtid does not exist in wtid_info!')

    altitude = wtid_info_i.loc[0, 'altitude']
    # =============wtid_info表:end =============

    com_sql = '''
            select 
            	wfid, 
            	wtid, 
            	windbin,
            	count(WTUR_WSpd_Ra_F32) as count,
            	AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
            	AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32
            from
            	(select 
            		wfid, 
            		wtid, 
            		ts_2, 
            		WTUR_WSpd_Ra_F32, 
            		WTUR_PwrAt_Ra_F32,
            		count,
            		WTUR_State_Rn_I8,
            		round(WTUR_WSpd_Ra_F32/0.5+0.00000001)*0.5 as windbin 
            	from 
            		(select 
            			wfid, 
            			wtid, 
            			ts_2, 
            			AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
            			AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32, 
            			AVG(WTUR_State_Rn_I8) as WTUR_State_Rn_I8,
            			count(WTUR_WSpd_Ra_F32) as count
            		from 
            			(select
            				wfid, 
            				wtid, 
            				ts_2,
            				WTUR_WSpd_Ra_F32*pow((1.293*pow(10,(-(altitude/(18400*(1+(1/273.15)*WTUR_Temp_Ra_F32)))))/(1+(1/273.15)*WTUR_Temp_Ra_F32)/density),(1/3)) as WTUR_WSpd_Ra_F32,
            				WTUR_PwrAt_Ra_F32,  
            				WTUR_State_Rn_I8
            			from(
            				SELECT
            					{density} as density,
            					{altitude} as altitude,
            					wfid, 
            					wtid, 
            					WTUR_WSpd_Ra_F32,
            					WTUR_PwrAt_Ra_F32, 
            					WTUR_Temp_Ra_F32,
            					WTUR_State_Rn_I8,
            					concat(substring(ts,1,15),'0:00') AS ts_2 
            				from 
            					md4x_public_all_20200701101328566  
            				where 
            					wtid >='{wtid_start}' and wtid<='{wtid_end}'
            					and ts >= '{date_start}' 
            					and ts < '{date_end}'
            				)tt
            			)t  
            		GROUP BY(wfid, wtid, ts_2)  
            		)t2 
            	where 
            		WTUR_State_Rn_I8 > 0.9 
            		and count > 30
            	)t3
            where count>=3
            GROUP BY (wfid, wtid, windbin)
            order by (wfid, wtid, windbin)
    '''

    # 每仓符合度10min输入数据(处理后的)
    com_sql = com_sql.format(wtid_start=wtid_start, wtid_end=wtid_end,date_start=date_start,date_end=date_end, density=density, altitude=altitude)
    data_10min_4_compute_com = aws_helper.execute_query_aws(db, com_sql)

    # merge gua_pwr_i后，去掉不满足条件的风速仓
    data_10min_4_compute_com = pd.merge(data_10min_4_compute_com, gua_pwr_i, how='left', on=['wfid', 'wtid', 'windbin'])
    data_10min_4_compute_com = data_10min_4_compute_com.dropna()

    # 计算每仓符合度
    data_windbin_com = compute_com_process(data_10min_4_compute_com)

    com_k_capc = data_windbin_com.groupby(['wfid', 'wtid'])['comformity'].mean()
    com_k_capc = pd.DataFrame(com_k_capc)
    com_k_capc = com_k_capc.reset_index()

    # 计算k值
    com_k_capc['k_value'] = compute_k(data_10min_4_compute_com)
    # 计算capc
    com_k_capc['capc'] = compute_capc_process(data_windbin_com)

    result = result.append(com_k_capc)

    # data_windbin_com.to_csv(result_dir + com_k_cacp_result + str(data_7s.loc[0, 'wtid']) + '_4_1_com_windbin.csv', index=False)
    # com_k_capc.to_csv(result_dir + com_k_cacp_result + str(data_7s.loc[0, 'wtid']) + '_4_1_com_k_capc.csv', index=False)

    z.show(result)


# 1.读取文件
gua_pwr = pd.read_csv(input_dir + 'gua_pwr.csv', sep=',')
wtid_info = pd.read_csv(input_dir + 'wtid_info.csv', sep=',')

# 2.调用函数
com_k_capc_data_process(632500,'632500001','632500001','2019-01-01 00:00:00','2020-01-01 00:00:00',gua_pwr, wtid_info)
