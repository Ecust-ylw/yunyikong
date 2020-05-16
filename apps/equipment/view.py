from flask import render_template, request, jsonify
from models import Admin_people, Equipment, Equipment_alarm
from db import db
from datetime import datetime, timedelta


# 团队的设备管理界面，把所有设备对象传给前端
def show_page():
    data = {
        'equipments': Equipment.query.all(),
    }
    # now = datetime.now()
    # to_day = now.day
    # to_month = now.month
    # to_year = now.year
    # today = datetime(to_year, to_month, to_day)
    # tomorrow = today + timedelta(days=1)
    # yesterday = today - timedelta(days=1)
    alarms = Equipment_alarm.query.filter(Equipment_alarm.if_repired==False).order_by(
        Equipment_alarm.alarm_time.desc()).all()
    count = len(alarms)
    equipments = Equipment.query.all()
    equip = []
    for a in equipments:
        equip.append({
            'longitude': a.gaode_longitude,
            'latitude': a.gaode_latitude,
            'status': a.status,  # 该设备状态
        })
    return render_template('team/equipment.html', **data, alarms=alarms, count=count, equip=equip)


# 设备详情页面
def equipment_detail(eid):
    equipment = Equipment.query.filter(Equipment.id == eid).first()
    data = {
        'alarms_sure': [
            {
                'alarm_time': alarm.alarm_time,  # 报警
                'reason': alarm.reason,
                'id': alarm.id,  # id
                'if_repired':alarm.if_repired
            }
            for alarm in Equipment_alarm.query.filter(Equipment_alarm.equipment_id == eid,Equipment_alarm.if_repired==True).order_by(Equipment_alarm.alarm_time.desc()).all()
        ],
        'alarms_unsure': [
            {
                'alarm_time': alarm.alarm_time,  # 报警
                'reason': alarm.reason,
                'id': alarm.id,  # id
                'if_repired': alarm.if_repired
            }
            for alarm in Equipment_alarm.query.filter(Equipment_alarm.equipment_id == eid,
                                                      Equipment_alarm.if_repired ==False).order_by(
                Equipment_alarm.alarm_time.desc()).all()
        ],
        'location': equipment.location,
        'status': equipment.status,
        'admin': equipment.admin.name,
        'telephone': equipment.admin.telephone,
    }
    equipment_detail_id=equipment.id
    # now = datetime.now()
    # to_day = now.day
    # to_month = now.month
    # to_year = now.year
    # today = datetime(to_year, to_month, to_day)
    # tomorrow = today + timedelta(days=1)
    # yesterday = today - timedelta(days=1)
    alarms1 = Equipment_alarm.query.filter(Equipment_alarm.if_repired==False).order_by(
        Equipment_alarm.alarm_time.desc()).all()
    count = len(alarms1)
    return render_template('team/detail.html', **data, alarms1=alarms1, count=count,equipment_detail_id=equipment_detail_id)


# 修改设备信息界面
# def edit_page(eid):
#     equipment = Equipment.query.filter(Equipment.id == eid).first()
#     return render_template('team/edit_equipment.html', equipment=equipment)


# 修改设备信息
# def edit_equipment(eid):
#     equipment = Equipment.query.filter(Equipment.id == eid).first()
#     key = request.form.get('key')
#     value = request.form.get('value')
#     try:
#         if key == 'location':
#             equipment.location = value
#         elif key == 'status':
#             equipment.status = value
#         elif key == 'admin_id':
#             equipment.admin_id = value
#         elif key == 'gaode_longitude':
#             equipment.gaode_longitude = value
#         elif key == 'gaode_latitude':
#             equipment.gaode_latitude = value
#         db.session.commit()
#         return jsonify({'msg': 'success'})
#     except Exception as e:
#         print(e)
#         return jsonify({'msg': 'fail'})

# 修改设备信息时，返回设备数据
def edit_e(eid):
    e = Equipment.query.filter(Equipment.id == eid).first()
    data = {
        'location': e.location,
        'status': e.status,
        'gaode_longitude': float(e.gaode_longitude),
        'gaode_latitude': float(e.gaode_latitude),
        'id': e.id,
    }
    # print(data)
    return jsonify(data)


# 修改设备信息
def edit(eid):
    e = Equipment.query.filter(Equipment.id == eid).first()
    location = request.form.get('location')
    status = request.form.get('status')
    gaode_longitude = request.form.get('gaode_longitude')
    gaode_latitude = request.form.get('gaode_latitude')
    print(gaode_longitude,gaode_latitude)
    if status not in ['正常', '故障']:
        return jsonify({'msg': 'fail', 'error': '设备状态填写不符合规范！'})
    try:
        e.location = location
        e.status = status
        e.gaode_latitude = gaode_latitude
        e.gaode_longitude = gaode_longitude
        db.session.commit()
        return jsonify({'msg': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'error': '修改失败！'})


def add():
    admin = request.form.get('admin')
    location = request.form.get('location')
    status = request.form.get('status')
    gaode_latitude = request.form.get('gaode_latitude')
    gaode_longitude = request.form.get('gaode_longitude')
    admin = Admin_people.query.filter(Admin_people.name == admin).first()
    print(status)
    if not admin or admin.role_id != 3:
        return jsonify({'msg': 'fail', 'error': '管理员不存在！'})
    data = {
        'location': location,
        'status': status,
        'gaode_longitude': gaode_longitude,
        'gaode_latitude': gaode_latitude,
        'admin_id': admin.id,
    }
    try:
        e = Equipment(**data)
        db.session.add(e)
        db.session.commit()
        return jsonify({'msg': 'success'})
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'error': '添加失败！'})
