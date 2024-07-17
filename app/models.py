from app import db
from datetime import datetime
from app import db
class User_Details(db.Model):
    __tablename__ = 'User_Details'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(512), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    confirm_password = db.Column(db.String(512), nullable=False)
    create_at = db.Column(db.Date, default=datetime.now)


class User_Database(db.Model):
    __tablename__ = 'User_Database'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.Date, default=datetime.now())


class History(db.Model):
    __tablename__ = 'History'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('User_Database.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('User_Database.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
