% python
import matplotlib.pyplot as plt
import athena_helper as aws_helper


def plot(data_7s, data_10min, data_curve):
    """
    绘图：7s散点+实际曲线，10min散点+实际曲线，已剔除异常值
    :param data_7s: 7s数据
    :param data_10min: 10Min数据
    :param data_curve: 拟合曲线
    :return:
    """

    data_1 = data_7s[data_7s['WTUR_State_Rn_I8'] == 1]

    # 1 风速-功率
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WTUR_PwrAt_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("power [kW]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_1_win_pow_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WTUR_PwrAt_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTUR_PwrAt_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("power [kW]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_1_win_pow_10min.png', dpi=300)
    plt.close()

    # 2 风速-转速
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WGEN_Spd_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("generator speed [rpm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_2_win_gen_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WGEN_Spd_Ra_F32'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WGEN_Spd_Ra_F32'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("generator speed [rpm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_2_win_gen_10min.png', dpi=300)
    plt.close()

    # 3 风速-扭矩
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_3_win_tor_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_3_win_tor_10min.png', dpi=300)
    plt.close()

    # 4 转速-扭矩
    plt.figure()
    plt.scatter(data_1['WGEN_Spd_Ra_F32'], data_1['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("generator speed [rpm]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_4_gen_tor_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WGEN_Spd_Ra_F32'], data_10min['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], color='#E15759')
    plt.scatter(data_curve['WGEN_Spd_Ra_F32'], data_curve['WCNV_Other_Ra_F32_TorqueReference'], s=0.5, color='#E15759')
    plt.xlabel("generator speed [rpm]", fontproperties="STXihei")
    plt.ylabel("torque reference [kNm]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_4_gen_tor_10min.png', dpi=300)
    plt.close()

    # 5 风速-桨距角
    plt.figure()
    plt.scatter(data_1['WTUR_WSpd_Ra_F32'], data_1['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTPS_Ang_Ra_F32_blade1'], color='#E15759')
    plt.scatter(data_curve['WTUR_WSpd_Ra_F32'], data_curve['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("pitch angle [deg]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_5_win_pit_7s.png', dpi=300)
    plt.close()

    plt.figure()
    plt.scatter(data_10min['WTUR_WSpd_Ra_F32'], data_10min['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#4E79A7')
    plt.plot(data_curve['windbin'], data_curve['WTPS_Ang_Ra_F32_blade1'], color='#E15759')
    plt.scatter(data_curve['windbin'], data_curve['WTPS_Ang_Ra_F32_blade1'], s=0.5, color='#E15759')
    plt.xlabel("wind [m/s]", fontproperties="STXihei")
    plt.ylabel("pitch angle [deg]", fontproperties="STXihei")
    plt.grid()
    # plt.show()
    aws_helper.save_png_aws(plt, result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_5_win_pit_10min.png', dpi=300)
    plt.close()


def main_process(data_7s, data_10min, data_curve):
    """
    求机组的特性曲线和特性曲线散点图
    :param data_7s: 7s数据
    :param data_10min: 10min数据
    :param data_curve: 特性曲线数据
    :return:
    """
    # 保存文件
    data_curve.to_csv(result_dir + character_curve_result + str(data_7s.loc[0, 'wtid']) + '_3_1_character_curve.csv', index=False)
    # 调用绘图功能函数
    plot(data_7s, data_10min, data_curve)


def character_curve_data_process(wtid_start, wtid_end, date_start, date_end):
    sql_7s = '''
        SELECT 
        	wfid, 
        	wtid, 
        	ts, 
        	WTUR_WSpd_Ra_F32, 
        	WTUR_PwrAt_Ra_F32, 
        	WGEN_Spd_Ra_F32, 
        	WCNV_Other_Ra_F32_TorqueReference, 
        	WTPS_Ang_Ra_F32_blade1, 
        	WTUR_State_Rn_I8 
        from 
        	{table}  
        where 
        	wtid >='{wtid_start}' and wtid<='{wtid_end}' 
        	and ts >= '{date_start}' 
        	and ts < '{date_end}'
    '''

    sql_10min = '''
        select 
        	wfid, 
        	wtid, 
        	ts_2, 
        	WTUR_State_Rn_I8, 
        	WTUR_WSpd_Ra_F32, 
        	WTUR_PwrAt_Ra_F32,
        	WGEN_Spd_Ra_F32,
        	WCNV_Other_Ra_F32_TorqueReference,
        	WTPS_Ang_Ra_F32_blade1, 
        	count,
        	round(WTUR_WSpd_Ra_F32/0.5+0.00000001)*0.5 as windbin 
        from 
        	(select 
        		wfid, 
        		wtid, 
        		ts_2, 
        		AVG(WTUR_State_Rn_I8) as WTUR_State_Rn_I8, 
        		AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
        		AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32, 
        		AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32, 
        		AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference , 
        		AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1, 
        		count(WTUR_WSpd_Ra_F32) as count 
        	from 
        		(SELECT 
        			wfid, 
        			wtid, 
        			ts, 
        			WTUR_WSpd_Ra_F32, 
        			WTUR_PwrAt_Ra_F32, 
        			WGEN_Spd_Ra_F32, 
        			WCNV_Other_Ra_F32_TorqueReference, 
        			WTPS_Ang_Ra_F32_blade1, 
        			WTUR_State_Rn_I8,
        			concat(substring(ts,1,15),'0:00') AS ts_2 
        		from 
        			{table}  
        		where 
        			wtid >='{wtid_start}' and wtid<='{wtid_end}'
        			and ts >= '{date_start}'
        			and ts <= '{date_end}'
        		)t  
        	GROUP BY(wfid, wtid, ts_2)  
        	)t2 
        where 
        	WTUR_State_Rn_I8 > 0.9 
        	and count > 30
    '''

    sql_curve = '''
            select 
        	wfid, 
        	wtid, 
        	windbin,
        	count(WTUR_WSpd_Ra_F32) as count,
        	AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
        	AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32,
        	AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32,
        	AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference,
        	AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1
        from
        	(select 
        		wfid, 
        		wtid, 
        		WTUR_State_Rn_I8, 
        		WTUR_WSpd_Ra_F32, 
        		WTUR_PwrAt_Ra_F32,
        		WGEN_Spd_Ra_F32,
        		WCNV_Other_Ra_F32_TorqueReference,
        		WTPS_Ang_Ra_F32_blade1, 
        		count,
        		round(WTUR_WSpd_Ra_F32/0.5+0.00000001)*0.5 as windbin 
        	from 
        		(select 
        			wfid, 
        			wtid, 
        			ts_2, 
        			AVG(WTUR_State_Rn_I8) as WTUR_State_Rn_I8, 
        			AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
        			AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32, 
        			AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32, 
        			AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference , 
        			AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1, 
        			count(WTUR_WSpd_Ra_F32) as count 
        		from 
        			(SELECT 
        				wfid, 
        				wtid, 
        				ts, 
        				WTUR_WSpd_Ra_F32, 
        				WTUR_PwrAt_Ra_F32, 
        				WGEN_Spd_Ra_F32, 
        				WCNV_Other_Ra_F32_TorqueReference, 
        				WTPS_Ang_Ra_F32_blade1, 
        				WTUR_State_Rn_I8,
        				concat(substring(ts,1,15),'0:00') AS ts_2 
        			from 
        				{table}  
        			where 
        				wtid >='{wtid_start}' and wtid<='{wtid_end}'
        				and ts >= '{date_start}' 
        				and ts <= '{date_end}'
        			)t  
        		GROUP BY(wfid, wtid, ts_2)  
        		)t2 
        	where 
        		WTUR_State_Rn_I8 > 0.9 
        		and count > 30
        	)t3
        GROUP BY (wfid, wtid, windbin)
        order by (wfid, wtid, windbin)
    '''
    sql_7s = sql_7s.format(table=table, wtid_start=wtid_start, wtid_end=wtid_end, date_start=date_start, date_end=date_end)
    sql_10min = sql_10min.format(table=table, wtid_start=wtid_start, wtid_end=wtid_end, date_start=date_start, date_end=date_end)
    sql_curve = sql_curve.format(table=table, wtid_start=wtid_start, wtid_end=wtid_end, date_start=date_start, date_end=date_end)

    # data_7s = aws_helper.execute_query_aws(db, sql_7s)
    # data_10min = aws_helper.execute_query_aws(db, sql_10min)
    data_curve = aws_helper.execute_query_aws(db, sql_curve)

    z.show(data_curve)
    # main_process(data_7s, data_10min,data_curve)


def character_curve_data_process_correction(wtid_start, wtid_end, date_start, date_end, density, altitude):
    sql_7s_correction = '''
        select
            WTUR_WSpd_Ra_F32*pow((1.293*pow(10,(-(altitude/(18400*(1+(1/273.15)*WTUR_Temp_Ra_F32)))))/(1+(1/273.15)*WTUR_Temp_Ra_F32)/density),(1/3)) as WTUR_WSpd_Ra_F32,
            wfid, 
            wtid, 
            ts,
            WTUR_PwrAt_Ra_F32, 
            WGEN_Spd_Ra_F32, 
            WCNV_Other_Ra_F32_TorqueReference, 
            WTPS_Ang_Ra_F32_blade1, 
            WTUR_State_Rn_I8
        from(
        	SELECT
        		{density} as density,
        		{altitude} as altitude,
        		wfid, 
        		wtid, 
        		ts,
        		WTUR_WSpd_Ra_F32,
        		WTUR_Temp_Ra_F32,
        		WTUR_PwrAt_Ra_F32, 
        		WGEN_Spd_Ra_F32, 
        		WCNV_Other_Ra_F32_TorqueReference, 
        		WTPS_Ang_Ra_F32_blade1, 
        		WTUR_State_Rn_I8 
        	from 
        		{table}  
        	where 
        		wtid >='{wtid_start}' and wtid<='{wtid_end}'
        		and ts >= '{date_start}' 
        		and ts < '{date_end}'
        )t
    '''

    sql_10min_correction = '''
        select 
        	wfid, 
        	wtid, 
        	ts_2, 
        	WTUR_State_Rn_I8, 
        	WTUR_WSpd_Ra_F32, 
        	WTUR_PwrAt_Ra_F32,
        	WGEN_Spd_Ra_F32,
        	WCNV_Other_Ra_F32_TorqueReference,
        	WTPS_Ang_Ra_F32_blade1, 
        	count,
        	round(WTUR_WSpd_Ra_F32/0.5+0.00000001)*0.5 as windbin 
        from 
        	(select 
        		wfid, 
        		wtid, 
        		ts_2, 
        		AVG(WTUR_State_Rn_I8) as WTUR_State_Rn_I8, 
        		AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
        		AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32, 
        		AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32, 
        		AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference , 
        		AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1, 
        		count(WTUR_WSpd_Ra_F32) as count 
        	from 
        		(
        			select
        			WTUR_WSpd_Ra_F32*pow((1.293*pow(10,(-(altitude/(18400*(1+(1/273.15)*WTUR_Temp_Ra_F32)))))/(1+(1/273.15)*WTUR_Temp_Ra_F32)/density),(1/3)) as WTUR_WSpd_Ra_F32,
        			wfid, 
        			wtid, 
        			ts,
        			ts_2,
        			WTUR_PwrAt_Ra_F32, 
        			WGEN_Spd_Ra_F32, 
        			WCNV_Other_Ra_F32_TorqueReference, 
        			WTPS_Ang_Ra_F32_blade1, 
        			WTUR_State_Rn_I8
        			from(
        				SELECT
        					{density} as density,
        					{altitude} as altitude,
        					wfid, 
        					wtid, 
        					ts,
        					WTUR_WSpd_Ra_F32,
        					WTUR_Temp_Ra_F32,
        					WTUR_PwrAt_Ra_F32, 
        					WGEN_Spd_Ra_F32, 
        					WCNV_Other_Ra_F32_TorqueReference, 
        					WTPS_Ang_Ra_F32_blade1, 
        					WTUR_State_Rn_I8,
        					concat(substring(ts,1,15),'0:00') AS ts_2 
        				from 
        					{table}  
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
    '''

    sql_curve_correction = '''
        select 
        	wfid, 
        	wtid, 
        	windbin,
        	count(WTUR_WSpd_Ra_F32) as count,
        	AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
        	AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32,
        	AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32,
        	AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference,
        	AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1
        from
        	(select 
        		wfid, 
        		wtid, 
        		WTUR_State_Rn_I8, 
        		WTUR_WSpd_Ra_F32, 
        		WTUR_PwrAt_Ra_F32,
        		WGEN_Spd_Ra_F32,
        		WCNV_Other_Ra_F32_TorqueReference,
        		WTPS_Ang_Ra_F32_blade1, 
        		count,
        		round(WTUR_WSpd_Ra_F32/0.5+0.00000001)*0.5 as windbin 
        	from 
        		(select 
        			wfid, 
        			wtid, 
        			ts_2, 
        			AVG(WTUR_State_Rn_I8) as WTUR_State_Rn_I8, 
        			AVG(WTUR_WSpd_Ra_F32) as WTUR_WSpd_Ra_F32, 
        			AVG(WTUR_PwrAt_Ra_F32) as WTUR_PwrAt_Ra_F32, 
        			AVG(WGEN_Spd_Ra_F32) as WGEN_Spd_Ra_F32, 
        			AVG(WCNV_Other_Ra_F32_TorqueReference) as WCNV_Other_Ra_F32_TorqueReference , 
        			AVG(WTPS_Ang_Ra_F32_blade1) as WTPS_Ang_Ra_F32_blade1, 
        			count(WTUR_WSpd_Ra_F32) as count 
        		from 
        			(select
        				WTUR_WSpd_Ra_F32*pow((1.293*pow(10,(-(altitude/(18400*(1+(1/273.15)*WTUR_Temp_Ra_F32)))))/(1+(1/273.15)*WTUR_Temp_Ra_F32)/density),(1/3)) as WTUR_WSpd_Ra_F32,
        				wfid, 
        				wtid, 
        				ts,
        				ts_2,
        				WTUR_PwrAt_Ra_F32, 
        				WGEN_Spd_Ra_F32, 
        				WCNV_Other_Ra_F32_TorqueReference, 
        				WTPS_Ang_Ra_F32_blade1, 
        				WTUR_State_Rn_I8
        			from(
        				SELECT
        					{density} as density,
        					{altitude} as altitude,
        					wfid, 
        					wtid, 
        					ts,
        					WTUR_WSpd_Ra_F32,
        					WTUR_Temp_Ra_F32,
        					WTUR_PwrAt_Ra_F32, 
        					WGEN_Spd_Ra_F32, 
        					WCNV_Other_Ra_F32_TorqueReference, 
        					WTPS_Ang_Ra_F32_blade1, 
        					WTUR_State_Rn_I8,
        					concat(substring(ts,1,15),'0:00') AS ts_2 
        				from 
        					{table}  
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
        GROUP BY (wfid, wtid, windbin) 
        order by (wfid, wtid, windbin)
    '''

    sql_7s_correction = sql_7s_correction.format(table=table, wtid_start=wtid_start, wtid_end=wtid_end, date_start=date_start, date_end=date_end,
                                                 density=density, altitude=altitude)
    sql_10min_correction = sql_10min_correction.format(table=table, wtid_start=wtid_start, wtid_end=wtid_end, date_start=date_start, date_end=date_end,
                                                       density=density, altitude=altitude)
    sql_curve_correction = sql_curve_correction.format(table=table, wtid_start=wtid_start, wtid_end=wtid_end, date_start=date_start, date_end=date_end,
                                                       density=density, altitude=altitude)

    print(sql_curve_correction)
    return

    data_7s_correction = aws_helper.execute_query_aws(db, sql_7s_correction)
    data_10min_correction = aws_helper.execute_query_aws(db, sql_10min_correction)
    data_curve_correction = aws_helper.execute_query_aws(db, sql_curve_correction)

    main_process(data_7s_correction, data_10min_correction, data_curve_correction)


character_curve_data_process('632500001', '632500010', '2019-01-01 00:00:00', '2020-01-01 00:00:00')
# character_curve_data_process_correction('632500001', '632500010','2019-01-01 00:00:00','2020-01-01 00:00:00',0.87,3200)