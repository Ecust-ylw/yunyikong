from flask import Blueprint, request
from apps.user import view
from decorate import login_required

user = Blueprint('user', __name__)


# 登录页面
@user.route('/login')
def login_page():
    return view.login_page()


# 学生登录
@user.route('/login/student', methods=['POST'])
def student_login():
    if request.method == 'POST':
        return view.student_login()


# 管理员登录
@user.route('/login/admin', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        return view.admin_login()


# 修改个人信息
@user.route('/edit', methods=['POST', 'GET'])
@login_required
def edit_information():
    if request.method == 'GET':
        return view.edit_page()
    else:
        return view.edit_information()


@user.route('/edit2', methods=['POST', 'GET'])
def upload():
    return view.upload_post()


# 退出账号
@user.route('/logout')
def logout():
    return view.logout()
