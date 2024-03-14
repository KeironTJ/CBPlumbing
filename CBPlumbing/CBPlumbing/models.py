from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from CBPlumbing import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Customer(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    first_line_address = db.Column(db.String(120), index=True)
    second_line_address = db.Column(db.String(120), index=True)
    city = db.Column(db.String(120), index=True)
    county = db.Column(db.String(120), index=True)
    postal_code = db.Column(db.String(120), index=True)
    referal = db.Column(db.String(120), index=True)
    jobs = db.relationship('Job', backref='customer', lazy='dynamic')
    

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    job_type = db.Column(db.String(120), index=True)
    job_status = db.Column(db.String(120), index=True)
    job_notes = db.Column(db.String(240), index=True)
    invoice_status = db.Column(db.String(120), index=True)
    
class JobItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    item_name = db.Column(db.String(120), index=True)
    item_description = db.Column(db.String(240), index=True)
    item_quantity = db.Column(db.Integer)
    item_cost = db.Column(db.Float)
    item_total = db.Column(db.Float)

    @hybrid_property
    def item_total(self):
        return self.item_quantity * self.item_cost
    
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))