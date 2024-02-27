"""
Routes and views for the flask application.
"""

from datetime import datetime

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from urllib.parse import urlsplit
import sqlalchemy as sa

from CBPlumbing import app, db
from CBPlumbing.forms import LoginForm, RegistrationForm, AddCustomerForm, AddJobForm
from CBPlumbing.models import User, Customer, Job, JobItem


@app.route('/')
@app.route('/index')
def index():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('dash')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/dash', methods=['GET', 'POST'])
@login_required
def dash():
    return render_template('dash.html', title='Dashboard')

@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    form=AddCustomerForm()
    if form.validate_on_submit():
        customer = Customer(first_name=form.first_name.data, 
                            last_name=form.last_name.data, 
                            phone=form.phone.data, 
                            email=form.email.data, 
                            first_line_address=form.first_line_address.data, 
                            second_line_address=form.second_line_address.data, 
                            city=form.city.data, 
                            county=form.county.data, 
                            postal_code=form.postal_code.data,
                            referal=form.referal.data)
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully!')
        return redirect(url_for('dash'))
    return render_template('add_customer.html', title='Add Customer', form=form)


@app.route('/view_all_customers', methods=['GET', 'POST'])
@login_required
def view_all_customers():
    customers = db.session.query(Customer).all()
    return render_template('view_all_customers.html', title='Customers', customers=customers)


@app.route('/view_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def view_customer(customer_id):
    customer = db.session.query(Customer).filter(Customer.id == customer_id).first()
    return render_template('view_customer.html', title='Customers', subtitle=f"{customer.first_name} {customer.last_name}", customer=customer)

@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        job = Job(customer_id=form.customer_id.data, 
                  job_type=form.job_type.data, 
                  job_description=form.job_description.data, 
                  job_status=form.job_status.data, 
                  job_notes=form.job_notes.data, 
                  job_cost=form.job_cost.data, 
                  job_invoice=form.job_invoice.data, 
                  job_invoice_date=form.job_invoice_date.data, 
                  job_invoice_paid=form.job_invoice_paid.data)
        db.session.add(job)
        db.session.commit()
        flash('Job added successfully!')
        return redirect(url_for('dash'))
    return render_template('add_job.html', title='Add Job', form=form)

@app.route('/view_all_jobs', methods=['GET', 'POST'])
@login_required
def view_all_jobs():
    jobs = db.session.query(Job).all()
    return render_template('view_all_jobs.html', title='Jobs', jobs=jobs)




