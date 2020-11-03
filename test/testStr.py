com_sql='''
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
        					%(density)f as density,
        					%(altitude)f as altitude,
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
        					wtid = '%(wtid)s'
        					and ts >= '2019-01-01 00:00:00' 
        					and ts < '2019-12-31 00:00:00'
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
com_sql=com_sql%dict(density=1.1,altitude=3200.1,wtid='632500001')
print(com_sql)