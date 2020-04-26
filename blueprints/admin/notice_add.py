from flask import Blueprint, jsonify, session, request

from hitapply.models import Notice
from hitapply.extensions import db

notice_add = Blueprint('notice_add', __name__)

@notice_add.route('', methods = ['POST'])
def Notice_add():
    account = session.get('admin_login')
    if account is None:
        return jsonify(code=-102, data={"tip": "用户未登录"})

    json_data = request.get_json(silent=True)

    if json_data is None:
        return jsonify(code=-101, data=None)
    notice = Notice()
    notice.title = json_data.get('title')
    notice.content = json_data.get('content')
    Notice(notice)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify(code=101, data={'tip': '数据库异常'})

    return jsonify(code=0, data={'tip': '新增公告成功'})