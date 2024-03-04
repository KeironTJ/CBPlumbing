from operator import itemgetter
from typing import Optional
from datetime import datetime, timezone

from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash

from CBPlumbing import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Customer(db.Model): 
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    first_line_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    second_line_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    county: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    postal_code: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    referal: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    

class Job(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    customer_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('customer.id'))
    customer: so.Mapped[Customer] = so.relationship('Customer', backref='jobs')
    job_created_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    job_planned_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    job_completed_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    job_status: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    job_notes: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    job_invoice: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    

class JobItem(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    job_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('job.id'))
    job: so.Mapped[Job] = so.relationship('Job', backref='job_items')
    item_created_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    item_planned_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    item_completed_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    item_type: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    item_description: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    item_notes: so.Mapped[str] = so.mapped_column(sa.String(240), index=True)  
    labour_hours: so.Mapped[float] = so.mapped_column(sa.Float(120), index=True)
    item_cost: so.Mapped[float] = so.mapped_column(sa.Float(120), index=True)
    item_quantity: so.Mapped[float] = so.mapped_column(sa.Float(120), index=True)
    

class Invoice(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    job_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('job.id'), nullable=False)
    job: so.Mapped[Job] = so.relationship('Job', backref='invoices')
    customer_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('customer.id'), nullable=False)
    customer: so.Mapped[Customer] = so.relationship('Customer', backref='invoices')
    invoice_created_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    iinvoice_due_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    invoice_completed_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    invoice_cost: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    invoice_margin: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    invoice_price: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    invoice_notes: so.Mapped[str] = so.mapped_column(sa.String(240), index=True)
    
    

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))