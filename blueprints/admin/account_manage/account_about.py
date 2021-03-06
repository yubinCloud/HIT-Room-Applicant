from flask import Blueprint, request, jsonify, session
from models import Administrator
from extensions import db
import hashlib

from common.utils import send_json


account_about = Blueprint('account_about', __name__)


@account_about.route('', methods=['GET', 'POST'])
# @adm_login_required(get_grades=(1, ), post_grades=(1, ))
def Adm_account():
    # 获取json
    if request.method == 'GET':  # 处理GET请求
        rev_json = request.args
        cur_account = session.get('admin_login')
        cur_admin = Administrator.query.filter(Administrator.account == cur_account).first()
        cur_org = cur_admin.org
        res = account_list_GET(rev_json, cur_org)
        if type(res) == list:  # 成功返回数据
            return jsonify(code=0, data=res)
        elif type(res) == tuple:  # 失败，返回提示信息
            code, tip = res
            return jsonify(code=code, data={'tip': tip})
    elif request.method == 'POST':  # 处理POST请求
        rev_json = request.get_json(silent=True)
        if rev_json is None:  # json为空
            return jsonify(code=-101, data=None)
        admin = Administrator()
        code, tip = admin_add(admin, rev_json)
        if code == -101:  # 缺少必需参数
            return jsonify(code=code, data={'tip': tip})

        # 根据发起本次操作的管理的org来决定本次添加的管理员的org
        opr_admin = Administrator.query.get(session.get('admin_login'))
        admin.org = opr_admin.org
        db.session.add(admin)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(code=101, data={'error': '数据库异常'})
        return jsonify(code=code, data={'tip': tip})  # 返回成功


@account_about.route('/num', methods=['GET'])
# @adm_login_required(get_grades=(1, ))
def Adm_account_num():
    """
    GET：获取账号数量
    :return:
    """
    cur_account = session.get('admin_login')
    cur_admin = Administrator.query.filter_by(account=cur_account).first()
    cur_org = cur_admin.org
    account_num = len(Administrator.query.filter(Administrator.org == cur_org).all())
    return jsonify(code=0, data={'num': account_num})


def account_list_GET(rev_json, cur_org):
    """
    处理GET请求
    :param rev_json: 接受的json数据，cur_org：执行目前操作的管理员
    :return: 运行正确时返回需要发送的json中的data字段的值，其type为列表
            若出现错误则返回一个元组，分别为需要发送给前端的code和data字段值
    """
    # 获取参数
    start_id, end_id = rev_json.get('start_id'), rev_json.get('end_id')
    if start_id is None or end_id is None:  # 检查是否缺失参数
        return -101, '缺少必需参数'
    try:
        start_id = int(start_id)
        end_id = int(end_id)
    except Exception:
        return send_json(-102, 'start_id 或 end_id 值错误')
    # 计算真正应返回的账号id范围
    db_count = Administrator.query.count()  # 账号的数量
    if start_id > db_count:
        return -102, '超过最大公告数量'
    if end_id > db_count:
        end_id = db_count
    # 从数据库中查询相应记录
    administrators = Administrator.query.offset(db_count - end_id).limit(end_id - start_id + 1).all()
    res = [dict(account=record.account, grade=record.grade, name=record.name, phone=record.phone)
           for record in administrators if record.org == cur_org]
    return res


def admin_add(admin, rev_json):
    """
    处理POST请求，向数据库添加数据
    :param admin: 数据库Administrator实例
    :param rev_json: 接收的json数据
    :return: (code, tip) 状态码及提示信息
    """
    account_, password_, grade_, name_, phone_, = rev_json.get('account'), rev_json.get('password'), \
                                                       rev_json.get('grade'), rev_json.get('name'), \
                                                       rev_json.get('phone')
    if None in (account_, password_, grade_):
        return -101, '缺少必需参数'
    admin.account = account_
    admin.password = hashlib.new('md5', password_.encode()).hexdigest()
    admin.grade = grade_
    if name_:
        admin.name = name_
    if phone_:
        admin.phone = phone_
    return 0, '新增管理员账号成功'
