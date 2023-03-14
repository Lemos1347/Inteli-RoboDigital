# Importing libraries
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from datetime import datetime
import os
import pymysql

#MySQL database credentials
host = os.environ['MYSQL_HOST'] or 'localhost:3306'
user = os.environ['MYSQL_USER'] or 'root'
password = os.environ['MYSQL_PASSWORD'] or 'rootpass12345'
database = os.environ['MYSQL_DATABASE'] or 'DOBOT'
database_uri = f"mysql+pymysql://{user}:{password}@{host}/{database}"

# App's config
app = Flask(__name__)
# Enable cors
CORS(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy() 
db.init_app(app)


# Creating Dobot class to control
class Dobot:
   def __init__(self) -> None:
      self.connected = False
      self.device = None

dobot_instance = Dobot()


#Defining routes
@app.get('/connect')
def handle_connect():
   import pydobot
   from serial.tools import list_ports

   available_ports = list_ports.comports()
   for port in available_ports:
      try:
         device = pydobot.Dobot(port=port.device, verbose=False)
         dobot_instance.device = device
         dobot_instance.connected = True
         print(f'Connected with success!')
         return True
      except:
            print(
               f"Wrong port: {port.device}, trying another one...")
            continue
   return False

@app.get('/pose')
def handle_pose():
   # if dobot_instance.connected == False:
   #    response = {"status": "denied", "reasson": "Dobot is not connected"}
   #    return make_response(jsonify(response), 404)
   from migrations import Positions
   # (x, y, z, r, j1, j2, j3, j4) = dobot_instance.device.pose()
   (x, y, z, r, j1, j2, j3, j4) = (1, 2, 3, 4, 5, 6, 7, 8)
   position = Positions(x=x, y=y, z=z, r=r, j1=j1, j2=j2, j3=j3, j4=j4)
   # with app.app_context():
   db.session.add(position)
   db.session.commit()
   response = {"status": "success", "message": "positon got with success!"}
   return make_response(jsonify(response), 200)

@app.get('/all')
def handle_all():

   from migrations import Positions
   positions = db.session.scalars(db.select(Positions).order_by(desc(Positions.id))).all()
   response = []
   for position in positions:
      response.append(position.dict())
   
   # db.first_or_404(db.select(class).filter_by(row=var))
   return make_response(response, 200)

@app.get('/date/<string:date>')
def handle_date(date):
   from migrations import Positions
   try:
      date_compare = datetime.strptime(date, '%Y-%m-%d').date()
      positions = db.session.scalars(db.select(Positions).filter_by(date=date_compare).order_by(desc(Positions.id))).all()
      response = []
      for position in positions:
         response.append(position.dict())
      return make_response(response, 200)
   except Exception as err:
      response = {'type': 'error', 'message': f'{err}'}
      return make_response(jsonify(response), 500)

@app.get('/time/<string:time>')
def handle_time(time):
   from migrations import Positions
   try:
      time_compare = datetime.strptime(time, '%H:%M:%S').time()
      positions = db.session.scalars(db.select(Positions).filter_by(time=time_compare).order_by(desc(Positions.id))).all()
      response = []
      for position in positions:
         response.append(position.dict())
      return make_response(response, 200)
   except Exception as err:
      response = {'type': 'error', 'message': f'{err}'}
      return make_response(jsonify(response), 500)

@app.get('/id/<int:id>')
def handle_id(id):
   from migrations import Positions
   try:
      position = db.first_or_404(db.select(Positions).filter_by(id=id))
      response = position.dict()
      return make_response(response, 200)
   except Exception as err:
      response = {'type': 'error', 'message': f'{err}'}
      return make_response(jsonify(response), 500)


if __name__ == '__main__': 
   app.run(host='0.0.0.0', debug=True, port=3001)