from db import db
from datetime import datetime


# 每位学生的基本信息
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=True)  # 学号/职工号
    name = db.Column(db.String(100), nullable=True)     # 姓名
    password = db.Column(db.String(30), nullable=True)  # 密码
    telephone = db.Column(db.String(100), nullable=True)  # 用户电话
    gender = db.Column(db.String(10), nullable=True)  # 性别
    age = db.Column(db.String(10), nullable=True)  # 年龄
    address = db.Column(db.String(10), nullable=True)  # 籍贯
    temperature = db.Column(db.String(100))
    picture=db.Column(db.LargeBinary(length=4294967295))
    status = db.Column(db.Enum('正常', '异常', '疑似'), server_default='正常')
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), nullable=True)  # 宿舍楼-号
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=True)  # 班级
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=True)  # 学院
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)  # 角色信息

    classa = db.relationship('Class', backref=db.backref('students1'))  # 可以直接通过user._classa得到班级信息
    role = db.relationship('Role', backref=db.backref('users'))  # 可以直接通过user.role得到用户角色信息
    college = db.relationship('College', backref=db.backref('students2'))  # 直接通过user.college得到学院信息
    dormitory = db.relationship('Dormitory', backref=db.backref('students3'))  # 直接通过user.dormitory得到宿舍信息


class Admin_people(db.Model):
    __tablename__ = 'admin_people'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)  # 密码
    telephone = db.Column(db.String(30), nullable=False)  # 电话
    gender = db.Column(db.String(10), nullable=False)  # 性别
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)  # 角色信息

    role = db.relationship('Role', backref=db.backref('admins'))  # 可以直接通过user.role得到用户角色信息


# 班级信息
class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)  # 班级名称 专业-班级
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_people.id'))  # 辅导员id
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)  # 班级对应学院

    admin = db.relationship('Admin_people', backref=db.backref('classes1'))
    college = db.relationship('College', backref=db.backref('classes2'))


# 学院信息
class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_people.id'))

    admin = db.relationship('Admin_people', backref=db.backref('college1'), uselist=False)


# 宿舍信息
class Dormitory(db.Model):
    __tablename__ = 'dormitory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_people.id'))

    admin = db.relationship('Admin_people', backref=db.backref('dormitory1'))


# 角色信息
# 共5种：学生，辅导员，院系负责人，宿舍管理员，设备管理员
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    # if_add_student = db.Column(db.BOOLEAN, default=False)  # 是否可以添加学生
    # if_look_other = db.Column(db.BOOLEAN, default=False)  # 是否可以查看其他学生的体温信息
    # if_sure = db.Column(db.BOOLEAN, default=False)  # 是否可以确认该学生是否是病情导致的发热
    # if_drop_user = db.Column(db.BOOLEAN, default=False)  # 是否可以删除本来发热现已不发热的学生


# class Alarm_record(db.Model):
#     __tablename__ = 'alarm_record'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     alarm_time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 报警时间
#     temperature = db.Column(db.String(100))  # 温度大小
#     # 是否经过辅导员却认为发烧，默认为false，等到有人确认，值改为true，同时更新user_log中的status
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))  # 在何处检测到
#
#     user = db.relationship('User', backref=db.backref('alarm_records', lazy='dynamic'))
#     equipment = db.relationship('Equipment', backref=db.backref('alarm_records1'))


# 学生体温记录信息
class User_log(db.Model):
    __tablename__ = 'user_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 这里的id是每检测一个学生就会有一个id
    temperature = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)  # 检测时间
    status = db.Column(db.Enum('正常', '异常'), server_default='正常')
    if_sure = db.Column(db.BOOLEAN,default=False)  # 记录是否经过确认
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)  # 检测的仪器
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 后期查找时通过user_id来找到多次检测的信息

    user = db.relationship('User', backref=db.backref('user_logs'))
    equipment = db.relationship('Equipment', backref=db.backref('user_logs1'))


# 仪器信息
class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gaode_longitude = db.Column(db.DECIMAL(precision='15,6'))
    gaode_latitude = db.Column(db.DECIMAL(precision='15,6'))
    status = db.Column(db.Enum('正常', '故障'), server_default='正常')  # 设备状态
    location = db.Column(db.String(100))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_people.id'))  # 仪器管理者id

    admin = db.relationship('Admin_people', backref=db.backref('equipments'))


class Equipment_alarm(db.Model):  # 机器每异常一次就要写入记录表，修好后再写入一次记录
    __tablename__ = 'equipment_alarm'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alarm_time = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 报警时间
    reason = db.Column(db.TEXT)
    if_repired= db.Column(db.BOOLEAN,default=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))

    equipment = db.relationship('Equipment', backref=db.backref('equipment_alarms'))


class Equipment_log(db.Model):
    __tablename__ = 'equipment_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.Enum('正常', '异常'), server_default='正常')
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))

    equipment = db.relationship('Equipment', backref=db.backref('equipment_logs'))


