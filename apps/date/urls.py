from flask import Blueprint
from apps.date import view

date = Blueprint('date', __name__)


# 学生查看自己的体温记录，有时间
@date.route('/<time>')
def temperature_log(time):
    return view.temperature_log(time)


# 楼管查看学生体温记录
@date.route('/look/<uid>/<time>')
def look_temperature(uid,time):
    return view.look_temperature(uid,time)
