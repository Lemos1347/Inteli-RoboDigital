# Importing libraries
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pymysql

#MySQL database credentials
host = 'localhost:3306'
user = 'root'
password = 'rootpass12345'
database = 'DOBOT'
database_uri = f"mysql+pymysql://{user}:{password}@{host}/{database}"

# App's config function

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
   with app.app_context():
        db.session.add(position)
        db.session.commit()
   response = {"status": "success", "message": "positon got with success!"}
   return make_response(jsonify(response), 200)

@app.get('/all')
def handle_all():
   with app.app_context():
      from migrations import Positions
      positions = Positions.query.all()
   return make_response(positions, 200)

@app.get('/time/<string:time>')
def handle_time(time):
   from migrations import Positions
   with app.app_context():
      try:
         position = Positions.query.filter(Positions.time == time).all()
         return make_response(jsonify(position), 200)
      except Exception as err:
         return make_response(err, 500)

@app.get('/id/<int:id>')
def handle_id(id):
   from migrations import Positions
   try:
      position = Positions.query.filter(Positions.id == id).all()
      return make_response(jsonify(position), 200)
   except Exception as err:
      return make_response(jsonify(err), 500)


if __name__ == '__main__': 
   app.run(host='0.0.0.0', debug=True, port=3001)