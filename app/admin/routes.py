# create imports
from app import db
from app.models import User, Role, UserRoles
from flask import render_template, flash, redirect, url_for, request, session 
from flask_login import login_required, current_user 
from app.admin.decorators import admin_required
from app.admin import bp


## Admin Routes

# Displays the admin home page
@bp.route('/admin_home', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home():

    return render_template('admin/admin_home.html',
                           title='Admin Home')

# Displays the error page when a user is not an admin
@bp.route('/not_admin')
def not_admin():
    return render_template('admin/not_admin.html', title='Not Admin')


# Displays the admin roles page
@bp.route('/admin_users', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_users():

    users = db.session.query(User).all()
    roles = db.session.query(Role).all()
    user_roles = db.session.query(UserRoles).all()

    return render_template('admin/admin_users.html', 
                           title='Admin Users',
                           users=users, 
                           roles=roles, 
                           user_roles=user_roles)
