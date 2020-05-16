from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField


class upForm(FlaskForm):
    name = StringField('Name')
    file = FileField('file')
    submit = SubmitField('上传')

# 上传头像用到的类
