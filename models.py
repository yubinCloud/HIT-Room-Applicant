"""
数据库模型文件
"""

from hitapply.extensions import db


# 管理员账号信息表
class Administrator(db.Model):
    account = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.SmallInteger, nullable=False)
    name = db.Column(db.String(255))
    org = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))


# 公告信息表
class Notice(db.Model):
    notice_id = db.Column(db.String(255), primary_key=True, nullable=False)
    org = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text(255), nullable=False)


# 教室信息表
class Room(db.Model):
    room_id = db.Column(db.String(255), primary_key=True, nullable=False)
    building = db.Column(db.String(255), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    room_name = db.Column(db.String(255), nullable=False)
    org = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255))
    max_num = db.Column(db.Integer, nullable=False)
    permissible = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text)


# 时间表
class Timetable(db.Model):
    class_id = db.Column(db.Integer, primary_key=True, nullable=False)
    begin_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)


# 预约信息表
class Apply(db.Model):
    apply_id = db.Column(db.String(255), primary_key=True, nullable=False)
    activity_name = db.Column(db.String(255), nullable=False)
    applicant_id = db.Column(db.String(255), nullable=False)
    applicant_name = db.Column(db.String(255), nullable=False)
    applicant_phone = db.Column(db.String(255), nullable=False)
    apply_time = db.Column(db.DateTime, nullable=False)
    use_date = db.Column(db.String(255), nullable=False)
    begin_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    people_count = db.Column(db.Integer, nullable=False)
    request = db.Column(db.Text)
    org = db.Column(db.String(255))
    teacher_name = db.Column(db.String(255), nullable=False)
    material = db.Column(db.String(255))
    check_status = db.Column(db.Enum('待审核', '审核通过', '审核失败'), nullable=False)
    note = db.Column(db.Text)
    verifier_name = db.Column(db.String(255))
    building = db.Column(db.String(255))
    floor = db.Column(db.Integer)
    room_name = db.Column(db.String(255), default="不指定")