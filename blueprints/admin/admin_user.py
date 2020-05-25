from flask import Blueprint, jsonify, session
from hitapply.common.functions import adm_login_required
from hitapply.models import Administrator


admin_user = Blueprint('admin_user', __name__)


@admin_user.route('', methods=['GET'])
@adm_login_required(get_grades=(1, 2, 3))
def Admin_user():
    """
    GET：获取用户信息
    :return:
    """
    # 查找出当前管理员
    cur_account = session.get('admin_login')  # 获取当前用户名
    cur_admin = Administrator.query.filter_by(account=cur_account).first()
    if cur_admin is None:
        return jsonify(code=-102, tip='未查询到该管理员')

    res_data = admin_to_dict(cur_admin)
    return jsonify(code=0, data=res_data)


def admin_to_dict(admin):
    """
    将一个admin转化为一个字典，其中包含该用户的信息
    :param admin: 待转化的管理员对象
    :return: 转化后的字典
    """
    return dict(name=admin.name,
                account=admin.account,
                grade=admin.grade,
                org=admin.org,
                phone=admin.phone)