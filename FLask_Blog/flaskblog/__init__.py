import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_mail import Mail # mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# setting up a mail configuration 
app.config['MAIL_SERVER'] = 'smpt.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_PASS')
mail = Mail(app) # initializing 




from flaskblog import routes