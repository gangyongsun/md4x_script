#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 10:09
# @Author  : yonggang
# @Software: PyCharm

from _datetime import datetime  # python3解释器自带datetime模块

newsTime = 'Sun, 23 Apr 2017 05:15:05 GMT'

# Apr，Sept等月份简写的占位符是%b, 而03，04这些月份数字的占位符是%m
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

gmt_time = datetime.strptime(newsTime, GMT_FORMAT)
print(gmt_time)

# beijing_time = datetime.datetime.strptime(newsTime, BAI_FORMAT) + datetime.timedelta(hours=8)
# print(beijing_time)


# 把字符串转换成日期
time = datetime.strptime('2018-4-19 11:19:59', '%Y-%m-%d %H:%M:%S')  # 把字符串转换成时间
print(time)  # 输出时间信息

# 把日期转换成字符串
str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间并转化成字符串
print(str)  # 输出字符串信息

dt = datetime.now()
print('时间：(%Y-%m-%d %H:%M:%S %f): ', dt.strftime('%Y-%m-%d %H:%M:%S %f'))
print('时间：(%Y-%m-%d %H:%M:%S %p): ', dt.strftime('%y-%m-%d %I:%M:%S %p'))
print('星期缩写%%a: %s ' % dt.strftime('%a'))
print('星期全拼%%A: %s ' % dt.strftime('%A'))
print('月份缩写%%b: %s ' % dt.strftime('%b'))
print('月份全批%%B: %s ' % dt.strftime('%B'))
print('日期时间%%c: %s ' % dt.strftime('%c'))
print('今周是今年的第%s周(以周日为第一天)' % dt.strftime('%U'))
print('这周是今年的第%s周(以周一为第一天)' % dt.strftime('%W'))
print('今天是这周的第%s天 ' % dt.strftime('%w'))
print('今天是今年的第%s天 ' % dt.strftime('%j'))
print('今天是当月的第%s天 ' % dt.strftime('%d'))
print('当前日期：%s ' % dt.strftime('%x'))
print('当前时间：%s ' % dt.strftime('%X'))
print('今年是哪一年：%s ' % dt.strftime('%y'))
print('今年是哪一年：%s ' % dt.strftime('%Y'))
print('月：%s ' % dt.strftime('%m'))
print('小时(24)：%s ' % dt.strftime('%H'))
print('小时(12)：%s ' % dt.strftime('%l'))
print('分钟：%s ' % dt.strftime('%M'))
print('秒数：%s ' % dt.strftime('%S'))
print('微秒：%s ' % dt.strftime('%f'))
print('上午还是下午：%s ' % dt.strftime('%P'))
