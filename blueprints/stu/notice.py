"""
完成“查看公告列表”和“查看公告详情”的功能
查看公告列表：
    http://xx.com/api/stu/notice
    对应 @notice.route('', methods=['GET'])
查看公告详情：
    http://xx.com/api/stu/notice/id
    对应 @notice.route('/<string:notice_id>', methods=['GET'])
"""
from flask import Blueprint, jsonify, request
from models import Notice
from extensions import db



# 注册Blueprint
notice = Blueprint('notice', __name__)


# 查看公告详情
@notice.route('/<string:notice_id>', methods=['GET'])
def Notice_Info(notice_id):
    """
    查看公告详情，url为http://xx.com/api/stu/notice/id
    :param notice_id: 字符串，'id'或者数字字符串，'id'表示获取最新公告，数字字符串表示获取特定id的公告
    :return: 示例如下：
        {
            "code": 0,
            "data": {
                "author": "学工处",
                ........
            }
        }
            或者：
        {
            "code": 101,
            "data": {
                "tip": "数据库查询失败"
            }
        }
    """
    if notice_id == '-1':
        record = Notice.query.all()[-1]
        if record is None:
            return jsonify(code=101, data={'tip': '数据库查询失败'})
        else:
            data = {
                'id': record.notice_id,
                'author': record.org,
                'title': record.title,
                'time': record.time.strftime('%Y-%m-%d'),
                "text": record.content
            }
            return jsonify(code=0, data=data)
    else:
        record = Notice.query.get(notice_id)
        if record is None:
            return jsonify(code=101, data={'tip': '数据库查询失败'})
        else:
            data = {
                'id': record.notice_id,
                'author': record.org,
                'title': record.title,
                'time': record.time.strftime('%Y-%m-%d'),
                "text": record.content
            }
            return jsonify(code=0, data=data)


# 查看公告列表
@notice.route('', methods=['GET'])
def Notice_List():
    """
    查看公告列表，请求方式为GET，
    接收json文件，示例：
    {
        "startid":1,
        "endid":16
    }
    :return:从startid到endid的公告
    """
    start_id = int(request.args.get('startid'))
    end_id = int(request.args.get('endid'))
    if start_id and end_id:
        index = start_id
        data = []
        flag = 0    # 当有部分id在数据库中查不到时置为1
        while index <= end_id:
            index_str = str(index)
            record = Notice.query.filter(Notice.notice_id == index_str).first()
            if record:
                temp = {
                    'id': record.notice_id,
                    'title': record.title,
                    'time': record.time.strftime('%Y-%m-%d')
                }
                data.append(temp)
            else:
                flag = 1
            index += 1
        if flag == 1 and data == []:  # 查询不到
            return jsonify(code=101, data={'tip': '数据库查询失败'})
        return jsonify(code=0, data=data)
    else:
        return jsonify(code=-101, data={'tip': '缺少必要参数'})