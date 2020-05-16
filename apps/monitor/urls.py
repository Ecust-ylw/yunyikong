from flask import Blueprint, request
from apps.monitor import view
from decorate import login_required

monitor = Blueprint('monitor', __name__)


# 报警记录页面
@monitor.route('/alarm_records/<time>')
@login_required
def user_alarm_records(time):
    return view.user_alarm_records(time)



# 确认报警记录
@monitor.route('/confirm/<aid>')
@login_required
def confirm_alarm(aid):
    return view.confirm_alarm(aid)


# 删除报警记录
@monitor.route('/delete/<aid>')
@login_required
def delete_alarm(aid):
    return view.delete_alarm(aid)


# 人员状态页面
@monitor.route('/person_status')
@login_required
def person_status():
    return view.person_status()


# 删除学生绑定的宿舍号
@monitor.route('/drop/<sid>')
@login_required
def delete_student(sid):
    return view.delete_student(sid)


# 修改学生信息
@monitor.route('/edit/<sid>', methods=['POST', 'GET'])
def edit(sid):
    if request.method == 'GET':
        return view.edit_student(sid)
    else:
        return view.edit(sid)


# 楼管添加学生
@monitor.route('/add_student', methods = ['POST'])
def add_student():
    return view.add_student()
