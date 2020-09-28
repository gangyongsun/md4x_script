import AthenaHelper as awsHelper

def exec_sql(db, sql):
    # 执行SQL查询
    data = awsHelper.execQuery(db, sql)
    return data
