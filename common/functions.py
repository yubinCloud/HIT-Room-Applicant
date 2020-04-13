"""
公共函数文件
"""

# 检查一个字典中是否有一系列的key
def check_key(aDict, *keys):
    for k in keys:
        if k in aDict:  # 存在该键
            continue
        else:  # 不存在该键，抛出KeyError异常
            raise KeyError


# 表示的时间的int型转换为字符串类型
# 例：传入 661，返回'11：01'
def turn_to_string(a):
    hour = int(a / 60)
    minute = a - hour * 60
    if minute < 10:
        minute_str = '0' + str(minute)
    else:
        minute_str = str(minute)
    if hour < 10:
        hour_str = '0' + str(hour)
    else:
        hour_str = str(hour)
    return hour_str + ':' + minute_str


# 表示的时间的字符串型转换为int类型
# 例：传入'11：01'，返回 661
def turn_to_int(a):
    time_str = a.split(':')
    hour = int(time_str[0])
    minute = int(time_str[1])
    return hour * 60 + minute
