from flask import Blueprint, jsonify, session

admin_logout = Blueprint('admin_logout', __name__)

@admin_logout.route('', methods = ['POST'])
def Admin_Logout():
    session.pop('admin_login', None);
    return jsonify(code=0, data={"tip": "已退出登录"})