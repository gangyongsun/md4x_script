#!/usr/bin/python

time_str = "2019-08-28 00:00:07.000"

data_part_1 = time_str.str[0:10]
data_part_2 = time_str.str[11:15]

new_data = time_str.str[0:10] + ' ' + time_str.str[11:15] + '0:00'

print(data_part_1)
print(data_part_2)

print(new_data)
