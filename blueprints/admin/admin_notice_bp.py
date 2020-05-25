from flask import Blueprint, jsonify, request, session
from hitapply.models import Notice
from hitapply.extensions import db
import datetime
from hitapply.common.functions import adm_login_required

admin_notice_bp = Blueprint('admin_notice_bp', __name__)


@admin_notice_bp.route('', methods=['GET', 'POST'])
# @adm_login_required(get_grades=(1, 2, 3), post_grades=(1, 2))
def Adm_notice():
    # 获取json
    rev_json = request.get_json(silent=True)
    if request.method == 'GET':
        # 处理GET请求
        res = notice_list_GET(rev_json)
        if type(res) is list:
            return jsonify(code=0, data=res)
        elif type(res) is tuple:
            code, tip = res
            return jsonify(code=code, data={'tip': tip})
    elif request.method == 'POST':
        # 处理POST请求
        if rev_json is None:
            return jsonify(code=-101, data=None)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        notice = Notice(notice_id=str(Notice.query.count() + 1),
                        org="学工处",
                        title=rev_json.get('title'),
                        time=time,
                        content=rev_json.get('content'))
        db.session.add(notice)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'error': '数据库异常'})

        return jsonify(code=0, data={'tip': '新增公告成功'})


@admin_notice_bp.route('/num', methods=['GET'])
# @adm_login_required(get_grades=(1, 2, 3))
def Notice_list_num():
    """
    GET：获取公告数量
    :return:
    """
    notice_num = Notice.query.count()
    return jsonify(code=0, data={'num': notice_num})


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
    notices = Notice.query.offset(db_count - end_id).limit(end_id - start_id + 1).all()
    res = [dict(id=record.notice_id, title=record.title, time=record.time)
           for record in notices]
    return res


