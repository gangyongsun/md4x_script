% python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def dataProcess():
    # 功能：求该机组的对风偏差
    result = pd.DataFrame(columns=['windbin', 'Duration[h]', 'YawError[deg]', 'wfid', 'wtid'])

    # 输入数组
    wtid_array = genNumArray(632500001, 632500010)

    for wtid in wtid_array:
        sql = '''
        SELECT wfid,
            wtid,
            ts,
            WTUR_WSpd_Ra_F32,
            WTUR_PwrAt_Ra_F32,
            WYAW_Wdir_Ra_F32,
            WTUR_State_Rn_I8,
            WTPS_Ang_Ra_F32_blade1
        FROM md4x_public_all_20200701101328566
        WHERE wtid = '632500001'
            AND ts >= '2019-01-01 00:00:00'
            AND ts < '2019-12-31 00:00:00'
            AND WTUR_State_Rn_I8 = 1
            AND WTPS_Ang_Ra_F32_blade1 < 2 
        '''

        # 执行查询获取7s数据
        sql = sql % dict(wtid=wtid)
        data = aws_helper.execute_query_aws(db, sql)
        return_data = yawerrorcal(data)
        result = result.append(return_data)
    z.show(result)


dataProcess()