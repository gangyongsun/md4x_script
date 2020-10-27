import athena_helper as aws_helper


def exec_sql(db, sql):
    '''
      执行 athena sql
      :param db: string aws athena库名
      :param sql: string sql
      :return: DataFrame 结果集
      '''
    data = aws_helper.execute_query_aws(db, sql)
    return data
