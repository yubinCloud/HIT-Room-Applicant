from flask import Blueprint, jsonify, session

from src.models import Administrator

user_info = Blueprint('user_info', __name__)


@user_info.route('', methods=['GET'])
def User_Info():
    account = session.get('admin_login')
    if account is None:
        return jsonify(code=-102, data={"tip": "用户未登录"})

    admin = Administrator.query.filter_by(account=account).first();
    if admin is None:
        return jsonify(code=-102, data={"tip": "账户不存在"})

    return jsonify(code=0, data={
        "username": admin.name,
        "account": admin.account,
        "grade": admin.grade,
        "org": admin.org,
        "phone": admin.phone
    })