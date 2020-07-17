from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '79d0b0b4f9691928a05ccffa2de178ad'
app.config['SQLALCHEMY_DATABASE_URI'] = '''sqlite:///PatientDB.db'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
port=5000


from PP import routes
