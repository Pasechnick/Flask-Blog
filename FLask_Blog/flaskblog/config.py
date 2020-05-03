import os

# we take all our configuration code from __init__.py file and move here to have ability to write config separately

# by putting all configuration values in a class
# allows us to have configuration in a single object and
# also allows us to use inheritance to create new config 
class Config: # those are constant variables 

    # we need to make this secret sting unavailable for others, so we need to make from then environmental variables like in the case with mail server  
    SECRET_KEY = '5e5b968d2e77c6d37d2b17ee2bc819de'
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'

    # setting up a mail configuration 
    MAIL_SERVER = 'smpt.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_USERNAME = os.environ.get('EMAIL_PASS')