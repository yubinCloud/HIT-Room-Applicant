import logging
import os

# 连接数据库的相关常量
class DatabaseConst:
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'DZXxh990719!'
    MYSQL_HOST = '101.200.236.147'
    MYSQL_PORT = '3306'
    MYSQL_DBNAME = 'hitapply'
    MYSQL_CHARSET = 'utf8'

# 日志
LOGGING = logging

# 图片存储的路径
PIC_BASIC_DIR = os.path.abspath(os.path.dirname(__file__)) + '/pic'