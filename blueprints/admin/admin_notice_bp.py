from flask import Blueprint, jsonify, request, session
from hitapply.models import Notice
from hitapply.extensions import db

admin_notice_bp = Blueprint('admin_notice_bp', __name__)


@admin_notice_bp.route('', methods=['GET', 'POST'])
def Adm_notice():
    # 获取json
    rev_json = request.get_json(silent=True)
    if request.method == 'GET':
        res = notice_list_GET(rev_json)
        if type(res) is list:
            return jsonify(code=0, data=res)
        elif type(res) is tuple:
            code, data = res
            return jsonify(code=code, data=data)
    elif request.method == 'POST':
        account = session.get('admin_login')
        if account is None:
            return jsonify(code=-102, data={"tip": "用户未登录"})
        if rev_json is None:
            return jsonify(code=-101, data=None)
        notice = Notice()
        notice.title = rev_json.get('title')
        notice.content = rev_json.get('content')
        Notice(notice)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'error': '数据库异常'})

        return jsonify(code=0, data={'tip': '新增公告成功'})

def notice_list_GET(rev_json):
    """
    处理GET请求
    :param rev_json: 接收的json数据
    :return: 运行正确时返回需要发送的json中的data字段的值，其type为列表
            若出现错误则返回一个元组，分别为需要发送给前端的code和data字段值
    """
    # 获取参数
    start_id, end_id = rev_json.get('start_id'), rev_json.get('end_id')
    if start_id is None or end_id is None:  # 检查是否缺失参数
        return -101, None
    # 计算真正应该返回的公告id范围
    db_count = Notice.query.count()  # 公告的数量
    if start_id > db_count:
        return -102, '超过最大公告数量'
    if end_id > db_count:
        end_id = db_count
    # 从数据库中查询相应记录
    notices = Notice.query.offset(db_count - end_id + 1).limit(end_id - start_id + 1).all()
    res = [dict(id=record.notice_id, title=record.title, time=record.time)
           for record in notices]
    return res


