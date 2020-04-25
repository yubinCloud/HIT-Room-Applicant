from flask import Flask
import os
import click

from hitapply.extensions import db
from hitapply.settings import config
from hitapply.blueprints.stu import time_get, notice_list, stu_apply, room_floor_get, stu_room_use, notice_info, \
    stu_apply_info, room_info, room_use_info
from hitapply.blueprints.admin import admin_login, admin_logout, user_info, admin_notice_bp



def create_app(config_name=None):
    """
    app的工厂函数
    :param config_name:
    :return: app
    """
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('hitapply')
    app.config.from_object(config[config_name])

    # 为app注册相关信息
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)


def register_commands(app):
    @app.cli.command()
    def initdb():
        db.create_all()
        click.echo('Initialized database.')


def register_blueprints(app):
    # http://xx.com/stu/apply/id
    # GET：我的申请详细内容
    # POST：修改申请内容
    app.register_blueprint(stu_apply_info.stu_apply_info, url_prefix='/api/stu/apply/<string:apply_id>')

    # http://xx.com/api/stu/room/use/id
    # GET: 教室使用说明
    app.register_blueprint(room_use_info.room_use_info, url_prefix='/api/stu/room/use/<string:room_id>')

    # http://xx.com/api/stu/room/id
    # GET: 查看教室介绍
    app.register_blueprint(room_info.room_info, url_prefix='/api/stu/room/<string:room_id>')

    # http://xx.com/stu/room/use
    # GET: 教室使用情况
    app.register_blueprint(stu_room_use.stu_room_use, url_prefix='/api/stu/room/use')

    # http://xx.com/api/stu/building
    # GET: 获取全部楼号
    app.register_blueprint(room_floor_get.room_floor_get, url_prefix='/api/stu/building')

    # http://xx.com/api/stu/timetable
    # GET: 获取时间表
    app.register_blueprint(time_get.time_get, url_prefix='/api/stu/timetable')

    # http://xx.com/api/stu/apply
    # POST: 学生提交教室申请
    # GET: 我的申请列表
    app.register_blueprint(stu_apply.stu_apply, url_prefix='/api/stu/apply')

    # http://xx.com/api/stu/notice
    # GET: 查看公告列表
    app.register_blueprint(notice_list.notice_list, url_prefix='/api/stu/notice')

    # http://xx.com/api/stu/notice/id
    # GET: 查看公告详情
    app.register_blueprint(notice_info.notice_info, url_prefix='/api/stu/notice/<int:notice_id>')

    # http://xx.com/api/admin/login
    # POST: 管理员登录系统
    app.register_blueprint(admin_login.admin_login, url_prefix='/api/admin/login')

    # http://xx.com/api/admin/logout
    # POST: 管理员退出登录
    app.register_blueprint(admin_logout.admin_logout, url_prefix='/api/admin/logout')

    # http://xx.com/api/admin/user
    # GET: 获取用户信息
    app.register_blueprint(user_info.user_info, url_prefix='/api/admin/user')

    # http://xx.com/api/admin/notice
    # GET: 查看公告列表
    app.register_blueprint(admin_notice_bp.admin_notice_bp, url_prefix='/api/admin/notice')