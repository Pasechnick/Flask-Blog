
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_mail import Mail 
from flaskblog.config import Config # importing configuration class 

# extentions:
# we do not need to put extentions here cuz we want them to be created from outside of this "create_app" functions
# but we still want be able initialize this extentions inside of the fn with the app
# !! so we going to initialize the extentions at the top of our file but without the app variable
db = SQLAlchemy() 
bcrypt = Bcrypt() 
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail() # initializing mail server




# this function will take an argument for what configuration object we want to use our app. As default will be "Config" object with all configurations we made lately 
def create_app(config_class=Config): 
    # we move creation of our app inside this fnc and we grab everything except extensions 
    # we do not need to put extentions here cuz we want them to be created from outside of this "create_app" functions
    # but we still want be able initialize this extentions inside of the fn with the app
    # !! so we going to initialize the extentions at the top of our file but without the app variable, 
    # and then inside of "create_app" function we initialize them with "init_app(app)" method
    app = Flask(__name__)
    app.config.from_object(Config) # getting configuration object

    # !! here we initialize our extentions 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # "users", "posts", "main" are names for an instance of our blueprint classes accordingly created
    from flaskblog.users.routes import users 
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    # now we can register that blueprints: and pass in that blueprints that we have imported - "users", "posts", "main"
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app # return the created app