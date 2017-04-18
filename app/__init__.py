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





app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'redsfsfsfsfis'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iliudvtufwsxft:2a29ed42a42bd79714862ec0933cd0d930db33b7f3dd25f4aefc83c4965f3ed6@ec2-174-129-37-15.compute-1.amazonaws.com:5432/dev672r87g0822'


db = SQLAlchemy(app)
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db', MigrateCommand)


from app import views , db