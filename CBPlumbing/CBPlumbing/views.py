from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from urllib.parse import urlsplit
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
import logging

from CBPlumbing import app, db
from CBPlumbing.forms import LoginForm, RegistrationForm, AddCustomerForm, JobForm, JobItemForm
from CBPlumbing.models import User, Customer, Job, JobItems
from config import QueryConfig


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
    form = AddCustomerForm()
    if form.validate_on_submit():
        customer = Customer()
        form.populate_obj(customer)
        db.session.add(customer)
        try:
            print("Adding Customer Now")
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print("Error when adding customer")
        flash('Customer added successfully!')
        return redirect(url_for('view_all_customers'))
    return render_template('add_customer.html', title='Add Customer', form=form)

@app.route('/edit_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = db.session.query(Customer).get(customer_id)
    if customer is None:
        flash('Customer not found!', 'error')
        return redirect(url_for('view_all_customers'))
    form = AddCustomerForm(obj=customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        flash('Customer updated successfully!')
        return redirect(url_for('view_customer', customer_id=customer_id))
    return render_template('edit_customer.html', form=form, title = 'Edit Customer', customer=customer, subtitle="Edit Customer")


@app.route('/view_all_customers', methods=['GET'])
@login_required
def view_all_customers():
    customers = []
    try:
        print("Executing view_all_customers function")
        customers = db.session.query(Customer).filter(Customer.customer_active == True).all()
    except Exception as e:
        print("error in view_all_customer", e)


    return render_template('view_all_customers.html', title='Customers', customers=customers)

@app.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def delete_customer(customer_id):
    customer = db.session.query(Customer).get(customer_id)
    if customer is None:
        flash('Customer not found!', 'error')
        return redirect(url_for('view_all_customers'))
    customer.customer_active = False
    db.session.commit()
    return redirect(url_for('view_all_customers'))


@app.route('/view_customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def view_customer(customer_id):
    customer = db.session.query(Customer).get(customer_id)
    if customer is None:
        flash('Customer not found!', 'error')
        return redirect(url_for('view_all_customers'))
    return render_template('view_customer.html', title='Customers', subtitle="View Customer", customer=customer)



@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    form.customer_id.choices = [(c.id, str(c.id) + ' - ' + c.first_name + ' ' + c.last_name) for c in Customer.query.all()]
    form.job_status.choices = [(status, status) for status in QueryConfig.JOB_STATUS_LIST]
    form.invoice_status.choices = [(status, status) for status in QueryConfig.INVOICE_STATUS_LIST]
    form.job_type.choices = [(type, type) for type in QueryConfig.JOB_TYPE_LIST]
    if form.validate_on_submit():
        job = Job(
            customer_id=form.customer_id.data, 
            job_type=form.job_type.data,
            job_status=form.job_status.data,
            job_notes=form.job_notes.data,
            invoice_status=form.invoice_status.data
        )
        db.session.add(job)           
        db.session.commit()
        flash('Job added successfully!')
        return redirect(url_for('edit_job', job_id=job.id))
    
    # Populate form with submitted data if validation fails
    form.process(obj=request.form)
    return render_template('add_job.html', form=form, title = 'Add Job')


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    job = db.session.query(Job).get(job_id)
    if job is None:
        flash('Job not found!', 'error')
        return redirect(url_for('view_all_jobs'))
    form = JobForm(obj=job)
    form.customer_id.choices = [(c.id, str(c.id) + ' - ' + c.first_name + ' ' + c.last_name) for c in Customer.query.all()]
    form.job_status.choices = [(status, status) for status in QueryConfig.JOB_STATUS_LIST]
    form.invoice_status.choices = [(status, status) for status in QueryConfig.INVOICE_STATUS_LIST]
    form.job_type.choices = [(type, type) for type in QueryConfig.JOB_TYPE_LIST]
    if form.validate_on_submit():
        form.populate_obj(job)
        db.session.commit()
        flash('Job updated successfully!')
        return redirect(url_for('view_job', job_id=job_id))
    return render_template('edit_job.html', form=form, title = 'Jobs',items=job.items, job=job, subtitle="Edit Job")


@app.route('/add_job_item/<int:job_id>', methods=['GET', 'POST'])
@login_required
def add_job_item(job_id):
    form = JobItemForm()
    if form.validate_on_submit():
        job_item = JobItems(
            job_id=job_id,
            item_name=form.item_name.data,
            item_description=form.item_description.data,
            item_quantity=form.item_quantity.data,
            item_cost=form.item_cost.data
        )
        db.session.add(job_item)           
        db.session.commit()
        flash('Job Item added successfully!')
        return redirect(url_for('edit_job', job_id=job_id))
    return render_template('add_job_item.html', form=form, title = 'Add Job Item', job_id=job_id)

@app.route('/edit_job_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_job_item(item_id):
    item = db.session.query(JobItems).get(item_id)
    if item is None:
        flash('Job item not found!', 'error')
        return redirect(url_for('view_all_jobs'))
    form = JobItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Job Item updated successfully!')
        return redirect(url_for('edit_job', job_id=item.job_id))
    return render_template('edit_job_item.html', form=form, title = 'Edit Job', item=item, job=item.job_id, subtitle="Edit Item", job_id=item.job_id)


@app.route('/delete_job_item/<int:item_id>', methods=['POST'])
@login_required
def delete_job_item(item_id):
    item = db.session.query(JobItems).get(item_id)
    if item:
        job_id = item.job_id
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!')
    else:
        flash('Item not found!', 'error')
    return redirect(url_for('edit_job', job_id=job_id))



@app.route('/view_all_jobs', methods=['GET'])
@login_required
def view_all_jobs():
    jobs = db.session.query(Job).all()
    return render_template('view_all_jobs.html', title='Jobs', jobs=jobs)



@app.route('/view_job/<int:job_id>', methods=['GET'])
@login_required
def view_job(job_id):
    job = db.session.query(Job).get(job_id)
    items = JobItems.query.filter_by(job_id=job_id).all()
    customer = None
    if job:
        customer = db.session.query(Customer).get(job.customer_id)
    return render_template('view_job.html', title='Jobs',items=items, subtitle="View Job", job=job, customer=customer)



@app.route('/delete_job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = db.session.query(Job).filter(Job.id == job_id).first()
    if job:
        job.job_status = 'Cancelled'
        db.session.commit()
        flash('Job status updated to Cancelled!')
    else:
        flash('Job not found!', 'error')
    return redirect(url_for('view_all_jobs'))



