% python
import athena_helper as aws_helper
import pandas as pd
import matplotlib.pyplot as plt


def plot(start_stop, start_2h, data):
    # 绘图
    # 1
    plt.figure()
    plt.scatter(start_2h['wind_mean'], start_2h['count'], s=6, color='#4E79A7')
    plt.xlabel("2h wind mean [m/s]", fontproperties="STXihei")
    plt.ylabel("start count", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    file_name = str(data.loc[0, 'wtid']) + '_4_1_wind2h_count.png'
    aws_helper.save_png_aws(plt, result_dir + start_stop_result + file_name, dpi=300)
    plt.close()

    # 2
    start = start_stop[start_stop['state'] == 'start']
    plt.figure()
    plt.scatter(start['wind_mean'], start['seconds'], s=6, color='#4E79A7')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("start duration [s]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    file_name = str(data.loc[0, 'wtid']) + '_4_1_wind_start_duration.png'
    aws_helper.save_png_aws(plt, result_dir + start_stop_result + file_name, dpi=300)
    plt.close()
    # 3
    stop = start_stop[start_stop['state'] == 'stop']
    plt.figure()
    plt.scatter(stop['wind_mean'], stop['seconds'], s=6, color='#4E79A7')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("stop duration [s]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    file_name = str(data.loc[0, 'wtid']) + '_4_1_wind_stop_duration.png'
    aws_helper.save_png_aws(plt, result_dir + start_stop_result + file_name, dpi=300)
    plt.close()


def main_process(state_count, data, limit):
    # 1. 前期处理：根据风机状态将数据切割，取出时长和时间范围，并判断是否连续
    data_1 = state_recognize(state_count, data, 'WTUR_TurSt_Rs_S')

    group_by_result = data_1.groupby(['wfid', 'wtid', 'WTUR_TurSt_Rs_S', 'WTUR_TurSt_Rs_S_slice'])

    result = group_by_result['ts_diff'].sum()

    result = pd.DataFrame(result)

    result['ts_diff_max'] = group_by_result['ts_diff'].max()
    result['ts_start'] = group_by_result['ts'].min()
    result['ts_end'] = group_by_result['ts'].max()
    result = result.reset_index()

    result['is_discontinue'] = [(1 if i > limit else 0) for i in result['ts_diff_max']]
    result = result.sort_values('WTUR_TurSt_Rs_S_slice')
    result = result.reset_index()

    result = result.drop('index', axis=1)
    result = result.rename(columns={'ts_diff': 'seconds'})

    # 2. 结果1：基于result统计起停机时长、时间范围、平均风速
    start_stop = start_stop_extract(result, data)  # 基于result取出起停机的时长、时间范围、平均风速

    # 3. 结果2：基于result统计起停机时长、时间范围、平均风速
    group_by_start_stop_sta = start_stop.groupby(['wfid', 'wtid', 'state'])

    start_stop_sta = group_by_start_stop_sta['wtid'].count()
    start_stop_sta = pd.DataFrame(start_stop_sta)
    start_stop_sta.columns = ['count']
    start_stop_sta['seconds_min'] = group_by_start_stop_sta['seconds'].min()
    start_stop_sta['seconds_max'] = group_by_start_stop_sta['seconds'].max()
    start_stop_sta['seconds_mean'] = group_by_start_stop_sta['seconds'].mean()
    start_stop_sta['seconds_3_1_min'] = group_by_start_stop_sta['seconds_3_1'].min()
    start_stop_sta['seconds_3_1_max'] = group_by_start_stop_sta['seconds_3_1'].max()
    start_stop_sta['seconds_3_1_mean'] = group_by_start_stop_sta['seconds_3_1'].mean()
    start_stop_sta['seconds_3_2_min'] = group_by_start_stop_sta['seconds_3_2'].min()
    start_stop_sta['seconds_3_2_max'] = group_by_start_stop_sta['seconds_3_2'].max()
    start_stop_sta['seconds_3_2_mean'] = group_by_start_stop_sta['seconds_3_2'].mean()
    start_stop_sta['seconds_4_min'] = group_by_start_stop_sta['seconds_4'].min()
    start_stop_sta['seconds_4_max'] = group_by_start_stop_sta['seconds_4'].max()
    start_stop_sta['seconds_4_mean'] = group_by_start_stop_sta['seconds_4'].mean()
    start_stop_sta = start_stop_sta.reset_index()

    # 4. 结果3：基于start_stop将时间按两小时切割，计算起机次数
    start_2h = start_2h_count(start_stop, data)

    # plot(start_stop, start_2h, data)

    return (start_stop)


def data_process(limit=200, wind_is_correct=0, wtid_info=[]):
    # 功能：用于启停机时长统计
    # 输入：
    #   limit——当时间间隔超过limit，则认为是间断点，不作统计；
    #   若wind_is_correct=1，则需输入wtid_info

    state_count_sql = '''
        SELECT count(DISTINCT WTUR_TurSt_Rs_S)
        FROM md4x_public_all_20200701101328566
        WHERE 
            wtid= '%(wtid)s'
            AND ts >= '2019-01-01 00:00:00'
            AND ts < '2019-12-31 00:00:00'
    '''

    sql = '''
        SELECT 
           	wfid,
           	wtid,
           	ts,
           	WTUR_WSpd_Ra_F32,
           	WTPS_Ang_Ra_F32_blade1, 
        	WTUR_TurSt_Rs_S,
           	CASE WHEN date_diff('second',nth_value(a.ts,CASE WHEN a.no-1<=0 THEN a.no ELSE a.no-1 end)
                                       OVER 
        							   (Partition By a.wtid ORDER BY no rows BETWEEN unbounded preceding AND unbounded following) ,a.ts) >=18
                  or date_diff('second',nth_value(a.ts,CASE WHEN a.no-1<=0 THEN a.no ELSE a.no-1 end)
                                       OVER 
        							   (Partition By a.wtid ORDER BY no rows BETWEEN unbounded preceding AND unbounded following) ,a.ts) =0 
           	THEN 8
           	ELSE date_diff('second',nth_value(a.ts,CASE WHEN a.no-1<=0 THEN a.no ELSE a.no-1 end) 
                                   	   OVER 
        						       (Partition By a.wtid ORDER BY no rows BETWEEN unbounded preceding AND unbounded following) ,a.ts)
           	END as ts_diff
        FROM 
         	(SELECT 
        		wfid, 
        		wtid, 
        		cast(substr(ts,1,19) AS timestamp) ts,
        		row_number() over(Partition By wtid ORDER BY wtid,ts) no,
        		WTUR_WSpd_Ra_F32, 
        		WTPS_Ang_Ra_F32_blade1, 
        		WTUR_TurSt_Rs_S 
        	from 
        		md4x_public_all_20200701101328566  
        	where 
        		wtid = '%(wtid)s'
        		and ts >= '2019-01-01 00:00:00' 
        		and ts < '2019-12-31 00:00:00'
        	order by ts
        ) a
	'''
    sql = '''
        SELECT
            wfid,
            wtid,
            wtur_turst_rs_s,
            min(ts) AS ts_start,
            max(ts) AS ts_end,
            sum(ts_diff) AS seconds,
            max(ts_diff) AS ts_diff_max
        FROM 
            (SELECT 
                wfid,
                wtid,
                cast(substr(ts,1,19) AS timestamp) ts,
                CASE
                    WHEN 
                        date_diff('second',cast(substr(lag(ts,1,ts) OVER (order by ts),1,19) AS timestamp),cast(substr(ts,1,19) AS timestamp))=0
                        OR
                        date_diff('second',cast(substr(lag(ts,1,ts) OVER (order by ts),1,19) AS timestamp),cast(substr(ts,1,19) AS timestamp))>16 
                    THEN 8
                    ELSE 
                        date_diff('second',cast(substr(lag(ts,1,ts) OVER (order by ts),1,19) AS timestamp),cast(substr(ts,1,19) AS timestamp))
                    END AS ts_diff , 
                    cast(wtur_turst_rs_s AS integer) AS wtur_turst_rs_s, 
                    row_number() OVER(ORDER BY ts)-row_number() OVER(PARTITION BY wtur_turst_rs_s ORDER BY  ts) AS no2
                FROM md4x_public_all_20200701101328566
                WHERE 
                    wtid = '%(wtid)s'
                    AND ts >= '2019-04-02 00:00:00'
                    AND ts < '2019-04-03 00:00:00'
                ORDER BY  wtid,ts )
            GROUP BY  
                wfid,wtid,wtur_turst_rs_s,no2
        '''
    sql = sql % dict(wtid=632500001)
    state_count_sql = state_count_sql % dict(wtid=632500001)

    data = aws_helper.execute_query_aws(db, sql)
    state_count = aws_helper.execute_query_aws(db, state_count_sql)

    start_stop = main_process(state_count, data, limit)
    z.show(start_stop)
    # start_stop.to_csv(result_dir + start_stop_result + str(data.loc[0, 'wtid']) + '_start_stop.csv', index=False)


data_process(limit=200, wind_is_correct=0, wtid_info=[])
