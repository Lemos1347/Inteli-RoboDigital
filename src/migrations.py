from __init__ import db, app, user, password
from sqlalchemy.sql import func
from datetime import datetime
import pymysql

class Positions(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    z = db.Column(db.Integer, nullable=False)
    r = db.Column(db.Integer, nullable=False)
    j1 = db.Column(db.Integer, nullable=False)
    j2 = db.Column(db.Integer, nullable=False)
    j3 = db.Column(db.Integer, nullable=False)
    j4 = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    time = db.Column(db.Time, nullable=False, default=datetime.now().time())
   #server_default=func.now()

conn = pymysql.connect(host='localhost', user=user, passwd=password, port=3306)
with conn.cursor() as cur:
    cur.execute('CREATE DATABASE IF NOT EXISTS DOBOT;')

with app.app_context():
   db.drop_all()
   db.create_all()

#(x, y, z, r, j1, j2, j3, j4) = self.device.pose()