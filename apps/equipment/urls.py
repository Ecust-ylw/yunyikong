from flask import request, Blueprint
from apps.equipment import view
from decorate import login_required

equipment = Blueprint('equipment', __name__)


# 修改设备
@equipment.route('/edit/<eid>', methods=['GET', 'POST'])
@login_required
def edit_equipment(eid):
    if request.method == 'GET':
        return view.edit_e(eid)
    else:
        return view.edit(eid)


# 展示所有设备
@equipment.route('/show')
@login_required
def equipment_show():
    return view.show_page()


# 设备详细信息
@equipment.route('/detail/<eid>')
@login_required
def equipment_detail(eid):
    return view.equipment_detail(eid)


@equipment.route('/add', methods=['POST'])
def add():
    return view.add()
