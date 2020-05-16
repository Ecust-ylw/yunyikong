from flask import render_template, request, session, jsonify
from models import Equipment, User_log, User, Equipment_log, Equipment_alarm, Admin_people, Class, College, Dormitory
from db import db
from datetime import datetime, timedelta


# 通过体温信息判断状态，并写入日志文件
def temperature_report(data):
    temperature = data.get('temperature')
    datetime = data.get('datetime')
    user_id = data.get('user_id')
    eid = data.get('eid')
    user = User.query.filter(User.id == user_id).first()
    equipment = Equipment.query.filter(Equipment.id == eid).first()
    if not equipment:
        return '输入了非法的eid'
    if not user:
        return '不存在该用户'
    if float(temperature) <= 37.3:
        status = '正常'
        reportdata = {
            'create_time': datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S'),
            'temperature': temperature,
            'status': status,
            'user_id': user_id,
            'equipment_id': eid,
        }
        try:
            report = User_log(**reportdata)
            db.session.add(report)
            user.temperature = temperature
            user.status = '正常'
            db.session.commit()
        except Exception as e:
            print(e)
    else:
        status = '异常'
        try:
            alarmdata = {
                'create_time': datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S'),
                'temperature': temperature,
                'user_id': user_id,
                'equipment_id': eid,
            }
            alarm = User_log(**alarmdata)
            db.session.add(alarm)
            user.status = '疑似'
            db.session.commit()
        except Exception as e:
            print(e)



# 通过设备信息判断状态，并写入日志文件
def equipment_report(data):
    code = data.get('code')  # 当前设备状态
    eid = data.get('eid')
    datetime = data.get('datetime')
    equipment = Equipment.query.filter(Equipment.id == eid).first()
    if code == '正常':
        reportdata = {
            'equipment_id': eid,
            'status': code,
            'create_time': datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S'),
        }
        try:
            report = Equipment_log(**reportdata)
            db.session.add(report)
            equipment.status = '正常'
            db.session.commit()
        except Exception as e:
            print(e)
    else:
        alarmdata = {
            'equipment_id': eid,
            'reason': code,
            'if_repired':False,
            'create_time': datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S'),
        }
        reportdata = {
            'equipment_id': eid,
            'status': code,
            'create_time': datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S'),
        }
        try:
            report = Equipment_log(**reportdata)
            alarm = Equipment_alarm(**alarmdata)
            db.session.add(report)
            db.session.add(alarm)
            equipment.status = '故障'
            db.session.commit()
        except Exception as e:
            print(e)



# 展示学生报警记录的页面
def user_alarm_records(time):
    user_id = session.get('id')
    grade = session.get('grade')
    if grade == 'admin':
        user = Admin_people.query.filter(Admin_people.id == user_id).first()
        now = datetime.now()
        to_day = now.day
        to_month = now.month
        to_year = now.year
        oneday=timedelta(days=1)
        begin_day = datetime(to_year, to_month, to_day) - oneday * 14
        today = datetime(to_year, to_month, to_day)
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)
        if user.role.id == 2:  # 辅导员
            data = {
                'alarms': [
                    {
                        'alarm_time': alarm.alarm_time,  # 报警时间
                        'temperature': alarm.temperature,  # 人员温度

                        'name': alarm.user.name
                    }
                    for classa in user.classes1 for student in classa.students1 for alarm in student.alarm_records
                ]
            }
        elif user.role.id == 3:  # 宿舍楼负责人,一人对应一台设备
            now = datetime.now()
            to_year = now.year
            find_time1 = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            find_year=find_time1.year
            find_month = find_time1.month
            find_day = find_time1.day
            find_time = datetime(find_year, find_month, find_day)
            find_tomorrow = find_time + timedelta(days=1)
            equipment = user.equipments[0]
            # 一个放查询日期确诊人id的列表
            today_id = []
            today_totals = User_log.query.filter(User_log.status == '异常',User_log.equipment_id == equipment.id,
                                                 User_log.create_time.between(find_time, find_tomorrow),
                                                 User_log.if_sure == True).all()
            for today_total in today_totals:
                if today_total.user_id not in today_id:
                    today_id.append(today_total.user_id)
            today_num = len(today_id)  # 查询当日确诊人数
            # 存放查询当日所有通过的人id的列表
            pass_id = []
            passes = User_log.query.filter(User_log.equipment_id == equipment.id,User_log.create_time.between(find_time, find_tomorrow)).all()
            for p in passes:
                if p.user_id not in pass_id:
                    pass_id.append(p.user_id)
            pass_num = len(pass_id)  # 查询当日内通过人数
            if pass_num==0:
                percentage=0
            else:
                percentage = today_num * 100 / pass_num  # 体温异常比例
            data = {
                'alarms_sure': [
                    {
                        'dormitory': alarm.user.dormitory.name if alarm.user.dormitory else '暂无宿舍',  # 宿舍名
                        'alarm_time': alarm.create_time,  # 报警时间
                        'temperature': alarm.temperature,  # 报警温度
                        'name': alarm.user.name,  # 学生姓名
                        'telephone': alarm.user.telephone,  # 学生电话
                        'id': alarm.id,  # id
                        'if_sure': alarm.if_sure,
                    }
                    for alarm in User_log.query.filter(User_log.equipment_id == equipment.id, User_log.status == '异常',
                                                       User_log.create_time.between(find_time, find_tomorrow),
                                                       User_log.if_sure == True).order_by(
                        User_log.create_time.desc()).all()
                ],
                'alarms_unsure': [
                    {
                        'dormitory': alarm.user.dormitory.name if alarm.user.dormitory else '暂无宿舍',  # 宿舍名
                        'alarm_time': alarm.create_time,  # 报警时间
                        'temperature': alarm.temperature,  # 报警温度
                        'name': alarm.user.name,  # 学生姓名
                        'telephone': alarm.user.telephone,  # 学生电话
                        'id': alarm.id,  # id
                        'if_sure': alarm.if_sure,
                    }
                    for alarm in User_log.query.filter(User_log.equipment_id == equipment.id, User_log.status == '异常',
                                                       User_log.create_time.between(find_time, find_tomorrow),
                                                       User_log.if_sure == False).order_by(
                        User_log.create_time.desc()).all()
                ],
                'today_num': today_num,
                'pass_num': pass_num,
                'percentage': percentage,
                'location': equipment.location,
            }
            alarms1 = User_log.query.filter(User_log.equipment_id == equipment.id, User_log.status == '异常',
                                            User_log.create_time.between(begin_day, tomorrow)).order_by(
                User_log.create_time.desc()).all()
            count = len(alarms1)
            time1 = time.split(' ')[0]
            twoweek = []
            for i in range(14):
                day = today - timedelta(days=i)
                twoweek.append(str(day).split(' ')[0])

            return render_template('louguan/alarm_record.html', **data, alarms1=alarms1,
                                   count=count,time=time1,twoweeks=twoweek,today_time=today)
        elif user.role.id == 4:  # 院负责人
            data = {
                'alarms': [
                    {
                        'name': alarm.user.name,
                        'alarm_time': alarm.alarm_time,
                        'temperature': alarm.temperature,
                    }
                    for student in user.college.first().students2 for alarm in student.alarm_records
                ]
            }
    else:
        return '您没有权限访问此页面'


# 展示设备报警记录的页面
# def equipment_alarm_page():
#     user_id = session.get('id')
#     grade = session.get('grade')
#     if grade == 'admin':
#         user = User.query.filter(User.id == user_id).first()
#         if user.role.id == 5:
#             data = {
#                 'alarm': [
#                     {
#                         'equipment_id': alarm.equipment_id,
#                         'reason': alarm.reason,
#                         'create_time': alarm.create_time
#                     }
#                     for equipment in user.equipments for alarm in equipment.equipment_alarms
#                 ]
#
#             }
#     else:
#         return '您没有权限查看此页面'


# 确认报警记录
def confirm_alarm(aid):
    id=session.get('id')
    user=Admin_people.query.filter(Admin_people.id==id).first()
    if user.role_id==3: #楼管
        alarm = User_log.query.filter(User_log.id == aid).first()
        try:
            alarm.user.status = '异常'
            alarm.user.temperature = alarm.temperature
            alarm.if_sure = True
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail'})
    else:
        alarm = Equipment_alarm.query.filter(Equipment_alarm.id == aid).first()
        try:
            alarm.equipment.status = '正常'
            alarm.if_repired = True
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail'})



# 删除报警记录
def delete_alarm(aid):
    id = session.get('id')
    user = Admin_people.query.filter(Admin_people.id == id).first()
    if user.role_id==3:
        alarm = User_log.query.filter(User_log.id == aid).first()

        try:
            db.session.delete(alarm)
            alarm.user.status = '正常'
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail'})
    else:
        alarm = Equipment_alarm.query.filter(Equipment_alarm.id == aid).first()
        try:
            db.session.delete(alarm)
            alarm.equipment.status = '正常'
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail'})



# 人员状态展示页面
def person_status():
    user_id = session.get('id')
    now = datetime.now()
    to_day = now.day
    to_month = now.month
    to_year = now.year
    today = datetime(to_year, to_month, to_day)
    user = Admin_people.query.filter(Admin_people.id == user_id).first()
    if user.role_id == 3:
        data = {
            'dormitorys': [
                [{
                    'name': stu.name,
                    'dormitory': stu.dormitory.name if stu.dormitory else '暂无宿舍',
                    'status': stu.status,
                    'temperature': stu.temperature if stu.temperature else '暂无体温',
                    'telephone': stu.telephone,
                    'id': stu.id,
                    'college': stu.college.name if stu.college else '暂无学院',
                    'class': stu.classa.name if stu.classa else '暂无班级',
                    'username': stu.username,
                    'time':today
                } for stu in dormitory.students3
                ] for dormitory in user.dormitory1
            ]
        }

        to_day = now.day
        to_month = now.month
        to_year = now.year
        oneday = timedelta(days=1)
        today = datetime(to_year, to_month, to_day)
        tomorrow = today + timedelta(days=1)
        begin_day = datetime(to_year, to_month, to_day) - oneday * 14
        equipment = user.equipments[0]
        alarms = User_log.query.filter(User_log.equipment_id == equipment.id, User_log.status == '异常',
                                       User_log.create_time.between(begin_day, tomorrow),
                                       ).order_by(User_log.create_time.desc()).all()
        count = len(alarms)
        return render_template('louguan/person.html', **data, alarms=alarms, count=count)
    elif user.role_id == 5:
        alls = []
        for college in College.query.filter(College.id == 1).all():
            college1 = []
            college1.append(college.name)
            for classi in college.classes2:
                classi1 = []
                classi1.append(classi.name)
                for s in classi.students1:
                    dormitory = s.dormitory.name if s.dormitory else '暂无宿舍'
                    temperature = s.temperature if s.temperature else '暂无数据'
                    collegea = s.college.name if s.college else '暂无学院'
                    classa = s.classa.name if s.classa else '暂无班级'
                    data = {
                        'username': s.username,
                        'name': s.name,
                        'gender': s.gender,
                        'status': s.status,
                        'dormitory': dormitory,
                        'temperature': temperature,
                        'college': collegea,
                        'class': classa,
                        'id': s.id,
                        'telephone': s.telephone
                    }
                    classi1.append(data)
                college1.append(classi1)
            alls.append(college1)
        now = datetime.now()
        to_day = now.day
        to_month = now.month
        to_year = now.year
        today = datetime(to_year, to_month, to_day)
        alarms = Equipment_alarm.query.filter(Equipment_alarm.if_repired==False).order_by(
            Equipment_alarm.alarm_time.desc()).all()
        count = len(alarms)
        time=now
        return render_template('team/person.html', all_students=alls, alarms=alarms, count=count,time=time)


# 删除学生的信息
def delete_student(id):
    sid = session.get('id')
    user = Admin_people.query.filter(Admin_people.id == sid).first()
    if user.role_id == 3:  # 楼管删除学生的宿舍号
        student = User.query.filter(User.id == id).first()
        try:
            student.dormitory_id = None
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'error': '删除失败！'})
    elif user.role_id == 5:  # 团队可以删除学生
        student = User.query.filter(User.id == id).first()
        try:
            db.session.delete(student)
            logs = User_log.query.filter(User_log.user_id == student.id).all()
            for log in logs:
                db.session.delete(log)
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'error': '删除失败！'})


# 要修改学生信息时，给前端发送学生数据
def edit_student(sid):
    id = session.get('id')
    user = Admin_people.query.filter(Admin_people.id == id).first()
    if user.role_id == 3:
        user = User.query.filter(User.id == sid).first()
        data = {
            'dormitory': user.dormitory.name if user.dormitory else '暂无宿舍',
            'id': user.id
        }
        return jsonify(data)
    elif user.role_id == 5:
        user = User.query.filter(User.id == sid).first()
        data = {
            'name': user.name,
            'dormitory': user.dormitory.name if user.dormitory else '暂无宿舍',
            'telephone': user.telephone,
            'gender': user.gender,
            'age': user.age,
            'address': user.address,
            'sid': user.id,
            'temperature': user.temperature if user.temperature else '暂无数据',
            'status': user.status,
            'class': user.classa.name if user.classa else '暂无班级',
            'college': user.college.name if user.college else '暂无学院',
            'username': user.username,
            'password': user.password
        }
        return jsonify(data)


# 修改学生信息
def edit(sid):
    id = session.get('id')
    user = Admin_people.query.filter(Admin_people.id == id).first()
    if user.role_id == 3:
        dormitory = request.form.get('dormitory')
        dormitory = Dormitory.query.filter(Dormitory.name == dormitory).first()
        user = User.query.filter(User.id == sid).first()
        if not dormitory:
            return jsonify({'msg': 'fail', 'error': '宿舍不存在!'})
        try:
            user.dormitory_id = dormitory.id
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'error': '修改失败!'})
    elif user.role_id == 5:
        name = request.form.get('name')
        dormitory = request.form.get('dormitory')
        telephone = request.form.get('telephone')
        gender = request.form.get('gender')
        age = request.form.get('age')
        address = request.form.get('address')
        temperature = request.form.get('temperature')
        status = request.form.get('status')
        classa = request.form.get('class')
        college = request.form.get('college')
        username = request.form.get('username')
        password = request.form.get('password')
        dormitory = Dormitory.query.filter(Dormitory.name == dormitory).first()
        classa = Class.query.filter(Class.name == classa).first()
        college = College.query.filter(College.name == college).first()
        if not dormitory:
            return jsonify({'msg': 'fail', 'error': '宿舍不存在!'})
        if not classa:
            return jsonify({'msg': 'fail', 'error': '班级不存在!'})
        if not college:
            return jsonify({'msg': 'fail', 'error': '学院不存在!'})
        user = User.query.filter(User.username == username, User.name == name).first()
        try:
            user.name = name
            user.username = username
            user.dormitory_id = dormitory.id
            user.telephone = telephone
            user.age = age
            user.gender = gender
            user.address = address
            user.temperature = temperature
            user.status = status
            user.class_id = classa.id
            user.college_id = college.id
            user.password = password
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'error': '修改失败!'})


def add_student():
    id = session.get('id')
    user = Admin_people.query.filter(Admin_people.id == id).first()
    if user.role_id == 3:
        name = request.form.get('name')
        username = request.form.get('username')
        dormitory = request.form.get('dormitory')
        user = User.query.filter(User.username == username, User.name == name).first()
        d = Dormitory.query.filter(Dormitory.name == dormitory).first()
        if not user:
            return jsonify({'msg': 'fail', 'error': '未找到符合条件的学生!'})
        if not d:
            return jsonify({'msg': 'fail', 'error': '宿舍不存在!'})
        try:
            user.dormitory_id = d.id
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'error': '添加失败!'})
    elif user.role_id == 5:
        name = request.form.get('name')
        dormitory = request.form.get('dormitory')
        telephone = request.form.get('telephone')
        gender = request.form.get('gender')
        age = request.form.get('age')
        address = request.form.get('address')
        temperature = request.form.get('temperature')
        status = request.form.get('status')
        classa = request.form.get('class')
        college = request.form.get('college')
        username = request.form.get('username')
        password = request.form.get('password')
        dormitory = Dormitory.query.filter(Dormitory.name == dormitory).first()
        classa = Class.query.filter(Class.name == classa).first()
        college = College.query.filter(College.name == college).first()
        if not dormitory:
            return jsonify({'msg': 'fail', 'error': '宿舍不存在!'})
        if not classa:
            return jsonify({'msg': 'fail', 'error': '班级不存在!'})
        if not college:
            return jsonify({'msg': 'fail', 'error': '学院不存在!'})
        if not (username and password):
            return jsonify({'msg': 'fail', 'error': '用户名和密码不能为空！'})
        data = {
            'name': name,
            'dormitory_id': dormitory.id,
            'telephone': telephone,
            'gender': gender,
            'age': age,
            'address': address,
            'role_id': 1,
            'temperature': temperature,
            'status': status,
            'class_id': classa.id,
            'college_id': college.id,
            'username': username,
            'password': password
        }
        if User.query.filter(User.username == username).first():
            return jsonify({'msg': 'fail', 'error': '该用户名已存在！'})
        try:
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            return jsonify({'msg': 'success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'error': '添加失败！'})
