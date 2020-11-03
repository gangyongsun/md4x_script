%python
import athena_helper as aws_helper

def data_integrity_process(wtid_start, wtid_end,date_start,date_end):
    sql = '''
    SELECT 
    	aa.wfid, 
    	aa.wtid,
        '{date_start}' as date_start,
    	'{date_end}' as date_end,
        MIN(aa.ts) as date_start_real,
    	max(aa.ts) as date_end_real,
        sum(aa.ts_diff)/3600.00 as hour,
        count(aa.ts) as line,
        sum(aa.ts_diff)/(date_diff('second',timestamp'{date_start}',timestamp'{date_end}')*1.00) as data_integrity,
        avg(aa.ts_diff) as sample_freq,
        sum(wtur_other_rn_i16_limpow)/(count(aa.ts)*1.00) as limpow_percent,
        sum(wtur_state_rn_i8)/(count(aa.ts)*1.00) as usable_percent
    FROM
       (SELECT 
    	   a.wfid,
           a.wtid,
           a.ts,
           a.wtur_other_rn_i16_limpow,
           a.wtur_state_rn_i8,
           CASE WHEN 
                date_diff('second',nth_value(a.ts,CASE WHEN a.no-1<=0 THEN a.no ELSE a.no-1 end) OVER (Partition By a.wtid ORDER BY no rows BETWEEN unbounded preceding AND unbounded following) ,a.ts) >=18
                or 
                date_diff('second',nth_value(a.ts,CASE WHEN a.no-1<=0 THEN a.no ELSE a.no-1 end) OVER (Partition By a.wtid ORDER BY no rows BETWEEN unbounded preceding AND unbounded following) ,a.ts) =0 
           THEN 8
           ELSE date_diff('second',nth_value(a.ts,CASE WHEN a.no-1<=0 THEN a.no ELSE a.no-1 end) OVER (Partition By a.wtid ORDER BY no rows BETWEEN unbounded preceding AND unbounded following) ,a.ts)
           END as ts_diff
       FROM 
         	(SELECT 
    		 	wfid,
             	wtid,
             	cast(substr(ts,1,19) AS timestamp) ts,
             	wtur_other_rn_i16_limpow,
             	wtur_state_rn_i8,
             	row_number() over(Partition By wtid ORDER BY wtid,ts) no
          	  FROM {table}
          	  WHERE wtid >='{wtid_start}' and wtid<='{wtid_end}'
                AND ts >= '{date_start}'
                AND ts < '{date_end}'
    		) a
       )aa
    group by aa.wfid,aa.wtid
    order by aa.wfid,aa.wtid
    '''

    #table:表名
    #wtid_start:开始的风机编号
    #wtid_end:结束的风机编号
    #date_start:抽取开始日期
    #date_end:抽取结束日期
    sql = sql.format(table=table,wtid_start=wtid_start, wtid_end=wtid_end,date_start=date_start,date_end=date_end)
    data = aws_helper.execute_query_aws(db, sql)
    return (data)

data = data_integrity_process('632500001', '632500010','2019-01-01 00:00:00','2020-01-01 00:00:00')
z.show(data)