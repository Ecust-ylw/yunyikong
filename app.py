from flask import Flask, session
import config
from models import User, Admin_people
from db import db

# from apps.manage.urls import manage
from apps.user.urls import user
from apps.monitor.urls import monitor
from apps.equipment.urls import equipment
from apps.index.urls import index
from apps.date.urls import date


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# app.register_blueprint(manage, url_prefix='/manage')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(monitor, url_prefix='/monitor')
app.register_blueprint(equipment, url_prefix='/equipment')
app.register_blueprint(index, url_prefix='/index')
app.register_blueprint(date, url_prefix='/date')


@app.context_processor
def my_context_processor():
    user_id = session.get('id')
    grade = session.get('grade')
    if grade == 'student':
        user = User.query.filter(user_id == User.id).first()
        if user:
            return {'user': user}
    else:
        user = Admin_people.query.filter(user_id == Admin_people.id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
