
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
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
    submit = SubmitField('Submit')
    

class JobForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int)
    job_status = SelectField('Job Status', validators=[DataRequired()])
    job_type = SelectField('Job Type', validators=[DataRequired()])
    job_notes = TextAreaField('Job Notes', validators=[Length(min=0, max=140)])
    invoice_status = SelectField('Invoice Status', validators=[DataRequired()])
    submit = SubmitField('Submit')