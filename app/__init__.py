import tempfile
import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import simplejson as json
from flask_session import Session
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from slugify import slugify
import psycopg2
import flask_whooshalchemy
from itsdangerous import URLSafeTimedSerializer, URLSafeSerializer, Signer, Serializer, BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer
from flask_httpauth import HTTPBasicAuth
from flask_jsonpify import jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

app = Flask(__name__)
bcrypt = Bcrypt(app)
sess = Session()

sess.init_app(app)




app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'redsfsfsfsfis'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
sess.init_app(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join( tempfile.gettempdir(), 'test1222.db')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)


from app import views , db

