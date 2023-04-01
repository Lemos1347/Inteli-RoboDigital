# Importing libraries
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
from datetime import datetime
import os
import pymysql

# *Caso não exista as variáveis de ambiente abaixo, serão utilizadas as informações estáticas do banco de dados*
try: 
   # Credenciais definidas nas variáveis de ambiente no docker-compose
   host = os.environ['MYSQL_HOST'] 
   user = os.environ['MYSQL_USER'] 
   password = os.environ['MYSQL_PASSWORD'] 
   database = os.environ['MYSQL_DATABASE']
   port = os.environ['MYSQL_MIGRATIONS_PORT']
   host_migrations = os.environ['MYSQL_MIGRATIONS_HOST']
except:
   # ------------------------------------------------------------------------------
   #
   # INSIRA AQUI AS CREDENCIAIS DO SEU BANCO DE DADOS CASO NÃO FOR RODAR COM DOCKER
   #
   # ------------------------------------------------------------------------------ 
   host = 'localhost:3306' # Url do host
   user = 'root' # Usuário de acesso do banco de dados
   password = 'rootpass12345' # Senha do usuário
   database = 'DOBOT' # Nome do banco de dados
   port = 3306 # Porta do servidor do banco de dados 
   host_migrations = 'localhost' # Ip/Endereço do banco de dados

# Uri completa do banco de dados (com o driver do mysql)
database_uri = f"mysql+pymysql://{user}:{password}@{host}/{database}"


# Instanciando um objeto Flask e passando seu constructor
app = Flask(__name__)
# Habilitando o cors nesse servidor
CORS(app)

# Configurando o dicionário para o flask_sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciando a conexão com o banco de dados MYSQL
db = SQLAlchemy() 
db.init_app(app)


# Criando uma classe de controle das informações do Dobot Magician Lite
class Dobot:
   # Propriedades do Dobot:
   #     Connected --> Saber se existe um robô conectado a máquina que está hosteado esse servidor
   #     Device --> resultado da instaciação da classe Dobot advinda da biblioteca pydobot   
   def __init__(self) -> None:
      self.connected = False
      self.device = None

# Criando um objeto Dobot
dobot_instance = Dobot()

# ---------------------------------------------------------------------
#                                ROTAS
#----------------------------------------------------------------------
# Rota para conectar o robo
@app.get('/connect')
def handle_connect():
   # Fazendo as importações necessárias
   import pydobot
   from serial.tools import list_ports

   # Pego todas as portas disponíveis na máquina que está rodando o servidor e faço um loop para testar cada uma. Apenas a porta do robô não dará erro e a conexão estará bem sucedida armazenada na propriedade 'device' do objeto 'dobot_instance'.
   available_ports = list_ports.comports()
   for port in available_ports:
      try:
         device = pydobot.Dobot(port=port.device, verbose=False)
         dobot_instance.device = device
         dobot_instance.connected = True
         print(f'Connected with success!')
         return jsonify({"type": "success", "message": "connected with sucess"}), 200
      except Exception as err:
            print(
               f"Wrong port: {port.device}, trying another one...")
            continue
   return jsonify({"type": "err", "message": "cannot connect"}), 500

# Rota para checar se há algum robô conectado
@app.get('/checkConnection')
def handle_checkConnection():
   # Checa se há algum robô conectado
   if dobot_instance.connected == True:
      return "Connected!", 200
   else:
      return "Not connected!", 500

# Rota para armazenar a posição atual do robô
@app.get('/pose')
def handle_pose():
   # Apenas armazenará a posição do robô caso exista um robô conectado
   if dobot_instance.connected == False:
      response = {"status": "denied", "reasson": "Dobot is not connected"}
      return jsonify(response), 404
   from migrations import Positions
   (x, y, z, r, j1, j2, j3, j4) = dobot_instance.device.pose()
   position = Positions(x=x, y=y, z=z, r=r, j1=j1, j2=j2, j3=j3, j4=j4)
   db.session.add(position)
   db.session.commit()
   response = {"status": "success", "message": "positon got with success!"}
   return jsonify(response), 200

# Rota para pegar todas as posições armazenadas no banco de dados
@app.get('/all')
def handle_all():
   # É utilizado o SQLAlchemy para conseguir todas as informações da tablela 'positions'
   from migrations import Positions
   # Pegando a posição do robô com o SQLAlchemy
   positions = db.session.scalars(db.select(Positions).order_by(desc(Positions.id))).all()
   # Formatando a resposta do ORM para enviar um JSON para o usuário
   response = []
   for position in positions:
      response.append(position.dict())

   return response, 200

# Rota para pegar uma posição que foi adicionada em uma data específica
@app.get('/date/<string:date>')
def handle_date(date):
   from migrations import Positions
   try:
      date_compare = datetime.strptime(date, '%Y-%m-%d').date()
      # Pegando a posição do robô com o SQLAlchemy
      positions = db.session.scalars(db.select(Positions).filter_by(date=date_compare).order_by(desc(Positions.id))).all()
      # Formatando a resposta do ORM para enviar um JSON para o usuário
      response = []
      for position in positions:
         response.append(position.dict())
      return response, 200
   except Exception as err:
      response = {'type': 'error', 'message': f'{err}'}
      return jsonify(response), 500

# Rota para pegar a posição que foi adicionada em um horário específico
@app.get('/time/<string:time>')
def handle_time(time):
   from migrations import Positions
   try:
      time_compare = datetime.strptime(time, '%H:%M:%S').time()
      # Pegando a posição do robô com o SQLAlchemy
      positions = db.session.scalars(db.select(Positions).filter_by(time=time_compare).order_by(desc(Positions.id))).all()
      # Formatando a resposta do ORM para enviar um JSON para o usuário
      response = []
      for position in positions:
         response.append(position.dict())
      return response, 200
   except Exception as err:
      response = {'type': 'error', 'message': f'{err}'}
      return jsonify(response), 500

# Rota para pegar uma posição específica com base no seu id na tabela 'positions'
@app.get('/id/<int:id>')
def handle_id(id):
   from migrations import Positions
   try:
      # Pegando a posição do robô com o SQLAlchemy
      position = db.first_or_404(db.select(Positions).filter_by(id=id))
      response = position.dict()
      return response, 200
   except Exception as err:
      response = {'type': 'error', 'message': f'{err}'}
      return jsonify(response), 500

# Rota para mover as juntas do robô para um ângulo específico caso algum robô esteja conectado
@app.post('/move')
def handle_move():
   # Checa se há algum robô conectado
   if dobot_instance.connected == False:
      response = {"status": "denied", "reasson": "Dobot is not connected"}
      return jsonify(response), 404
   # Importando o enum necessário para mover as juntas do robô
   from pydobot.enums import PTPMode

   # Pegando os dados enviados no formado json
   data = request.json
   # Movendo as juntas do robô
   dobot_instance.device._set_ptp_cmd(float(data['j1']), float(data['j2']), float(data['j3']), 0, wait=True, mode=PTPMode.MOVJ_ANGLE)
   response = {'type': 'success', 'message': 'Dobot moved'}
   return jsonify(response), 200


if __name__ == '__main__': 
   # Rodando o servidor
   app.run(host='0.0.0.0', debug=True, port=3001)