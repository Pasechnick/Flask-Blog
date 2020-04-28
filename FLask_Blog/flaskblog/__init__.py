from flask import Flask # we have removed all other imports excepts the Flask object (for "app = Flask(__name__)")
from flask_sqlalchemy import SQLAlchemy 
#we also need to import our routes, so the app can find those 



app = Flask(__name__)
app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app) 

from flaskblog import routes