from app.main import bp
from flask import render_template
from flask_login import login_required 

### The index view function
@bp.route('/')
@bp.route('/index')
def index():

    return render_template("main/index.html", title="Home")