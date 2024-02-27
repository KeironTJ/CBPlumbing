
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from CBPlumbing import db
from CBPlumbing.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class AddCustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_line_address = StringField('First Line Address', validators=[DataRequired()])
    second_line_address = StringField('Second Line Address')
    city = StringField('City', validators=[DataRequired()])
    county = StringField('County', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    referal = StringField('Referal')
    submit = SubmitField('Add Customer')
    
class AddJobForm(FlaskForm):
    customer_id = StringField('Customer ID', validators=[DataRequired()])
    job_type = StringField('Job Type', validators=[DataRequired()])
    job_description = StringField('Job Description', validators=[DataRequired()])
    job_status = StringField('Job Status', validators=[DataRequired()])
    job_notes = StringField('Job Notes')
    job_cost = StringField('Job Cost')
    job_invoice = StringField('Job Invoice')
    job_invoice_date = StringField('Job Invoice Date')
    job_invoice_paid = BooleanField('Job Invoice Paid')
    submit = SubmitField('Add Job')