"""
公共函数文件
"""
from flask import jsonify, session, request
import functools
import traceback
from datetime import datetime

from models import Administrator
from common import const

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


def adm_login_required(get_grades=(1, 2, 3), post_grades=(1, 2, 3)):
    """对管理员等级进行限制
    :param get_grades: GET请求时所允许的管理员等级
    :param post_grades: POST请求时所允许的管理员等级
    :return: 装饰后的视图函数
    """
    def login_decorator(view_func):
        """
        对func函数进行装饰
        :param view_func: 所要装饰的视图函数
        :return: 装饰后的视图函数
        """

        @functools.wraps(view_func)
        def wrapped_func(*args, **kwargs):
            """
            完成对管理员等级的验证，并转发参数给func
            :param args: 可变参数
            :param kwargs: 可变命名参数
            :return: 完成验证后的func，并将参数转发给func
            """
            account = session.get('admin_login')
            if account is None:  # 验证是否登录
                return jsonify(code=-102, data={'tip': '用户未登录'})
            cur_grade = Administrator.query.filter(Administrator.account == account).first()
            # 验证管理员等级
            if request.method == 'GET':
                if cur_grade not in get_grades:
                    return jsonify(code=-102, data={'tip': '管理员等级不符合要求'})
            else:
                if cur_grade not in post_grades:
                    return jsonify(code=-102, data={'tip': '管理员等级不符合要求'})

            return view_func(*args, **kwargs)

        return wrapped_func

    return login_decorator


def record_exception(exception: Exception):
    """
    将错误报告给日志
    :param exception: 产生的异常
    """
    const.LOGGING.warning(
        '{} occur a exception {}:\n{}\n==========\n{}'
            .format(datetime.now(), exception.__class__.__name__,exception.args, traceback.format_exc())
    )