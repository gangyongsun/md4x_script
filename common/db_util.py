import athena_helper as aws_helper

from config.property import db
from config.property import table


def exec_sql(db, sql):
    """
    执行 athena sql
    :param db: aws athena库名
    :param sql: sql语句
    :return: 结果集
    """
    return aws_helper.execute_query_aws(db, sql)


def prepare_data(wtid, start_time, end_time, columns, external_condition):
    """
    用AthenaSQL查询单个风机数据
    :param wtid: 风机ID
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param columns: sql选择的列
    :param external_condition: 外加where条件片段(例如："and WTUR_State_Rn_I8 = 1")
    :return: 数据
    """

    condition = " where wtid = '" + wtid + "' and ts >= '" + start_time + "' and ts <= '" + end_time + "' " + external_condition
    sql = "select " + columns + " from {0} " + condition
    sql = sql.format(table)
    data = aws_helper.execute_query_aws(db, sql)
    return (data)


def prepare_datas(wtid_head, wtid_tail, start_time, end_time, columns, external_condition):
    """
    用AthenaSQL查询多个风机数据
    :param wtid_head: 开始的风机ID
    :param wtid_tail: 结束的风机ID
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param columns: sql选择的列
    :param external_condition: 外加where条件片段(例如："and WTUR_State_Rn_I8 = 1")
    :return: 数据
    """

    condition = " where wtid >= '" + wtid_head + "' and wtid <= '" + wtid_tail + "' and ts >= '" + start_time + "' and ts <= '" + end_time + "' " + external_condition
    sql = "select " + columns + " from {0} " + condition
    sql = sql.format(table)
    data = aws_helper.execute_query_aws(db, sql)
    return (data)
