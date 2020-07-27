from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# Configurations
# ########Flask SQLALchemy
app.config['SECRET_KEY'] = '79d0b0b4f9691928a05ccffa2de178ad'
app.config['SQLALCHEMY_DATABASE_URI'] = '''sqlite:///PatientDB.db'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask Mail
gmail_user = 'devmails41@gmail.com'
gmail_pwd = 'this_ devs_mine'
SUBJECT = 'Account successfully created'

# ######## Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# Initializations
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
port = 5000

from PP import routes
