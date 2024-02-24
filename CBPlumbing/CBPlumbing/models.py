from typing import Optional

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
    

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))