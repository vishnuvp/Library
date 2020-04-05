from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'qwertyuiop'
app.config['LDAP_PROVIDER_URL'] = os.getenv('LDAP_URL','ldap://localhost:3893/')
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)
 
app.secret_key = 'some_random_key'
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
from bookinfo.auth.views import auth
app.register_blueprint(auth)
 
db.create_all()