from flask import Blueprint, jsonify, request, session

from hitapply.models import Administrator

import hashlib

admin_login = Blueprint('admin_login', __name__)

@admin_login.route('', methods = ['POST'])
def Admin_Login():
    username = request.json.get('username');
    password = request.json.get('password');
    if username is None or password is None:
        return jsonify(code=-101, data={"tip": "缺少必须参数"})

    # Convert password to md5
    password = hashlib.new('md5', password.encode()).hexdigest()

    admin = Administrator.query.filter(Administrator.account == username, 
                                       Administrator.password == password).first()
    if admin is None:
        return jsonify(code=-102, data={"tip": "用户名或密码错误，登陆失败"})
    else:
        session['admin_login'] = True
        return jsonify(code=0, data={"tip": "登陆成功"})