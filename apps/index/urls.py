from flask import Blueprint, render_template
from apps.index import view
from decorate import login_required

index = Blueprint('index', __name__)


@index.route('/')
@login_required
def index_page():
    return view.index()


