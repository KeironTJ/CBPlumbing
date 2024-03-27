
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, IntegerField, FloatField, DateField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import sqlalchemy as sa
from CBPlumbing import db
from CBPlumbing.models import User
from config import QueryConfig

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
    submit = SubmitField('Save')
    

class AddJobForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int)
    job_type = SelectField('Job Type', validators=[DataRequired()])  
    job_planned_date = DateField('Job Planned Date')
    job_notes = TextAreaField('Job Notes', validators=[Length(min=0, max=140)])
    submit = SubmitField('Save')
    
class EditJobForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int)
    job_status = SelectField('Job Status', validators=[DataRequired()])
    job_type = SelectField('Job Type', validators=[DataRequired()])
    job_notes = TextAreaField('Job Notes', validators=[Length(min=0, max=140)])
    invoice_status = SelectField('Invoice Status', validators=[DataRequired()])
    job_planned_date = DateField('Job Planned Date')
    job_completed_date = DateField('Job Completed Date')
    submit = SubmitField('Save')
    
class JobItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    item_description = TextAreaField('Item Description', validators=[Length(min=0, max=140)])
    item_quantity = IntegerField('Item Quantity', validators=[DataRequired()])
    item_cost = FloatField('Item Cost', validators=[DataRequired()])
    submit = SubmitField('Save')
    

class InvoiceForm(FlaskForm):
    job_id = IntegerField('Job ID', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[(type, type) for type in QueryConfig.INVOICE_STATUS_LIST])
