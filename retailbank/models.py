# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash

from retailbank import db
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import pytz
import tzlocal

local_timezone = tzlocal.get_localzone()
dt = datetime.utcnow()
local_time = dt.replace(tzinfo = pytz.utc).astimezone(local_timezone)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stake_holder = db.Column(db.Integer)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_ssn_id = db.Column(db.Integer, unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    last_updated = db.Column(
        db.DateTime(), default=local_time.now(), onupdate=local_time.now()
    )
    children = relationship("Account")


class Account(db.Model):
    customer_id = db.Column(db.Integer, ForeignKey('customer.customer_id'))
    account_id = db.Column(db.Integer, primary_key=True, nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(120), nullable=False)
    last_updated = db.Column(
        db.DateTime(), default=local_time.now(), onupdate=local_time.now()
    )
    children = relationship("Transaction")


class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, ForeignKey('account.account_id'))
    description = db.Column(db.String(120), nullable=False)
    date_of_transaction = db.Column(db.DateTime(), default=local_time.now())
    amount = db.Column(db.Integer, nullable=False)
