from flask import render_template, url_for, flash, redirect, request # we need "request" to 
from flaskblog import app, db, bcrypt # we need to import "db" and "bcrypt" to use that hash algorithm (remember that before we got the instance of bcrypt class with python3 shell)
from flaskblog.forms import RegistrationForm, LoginForm 
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required # imports that class so we can check the user email and password validation with the db data, and with current user we can deliver user a


posts = [
    {
        'author': 'corey schafer',
        'title': 'blog post 1',
        'content': 'First post content',
        'date_posted': 'april 20, 2002'
    },

    {
        'author': 'alex mitu',
        'title': 'blog post 2',
        'content': 'second post content',
        'date_posted': 'april 23, 2012'
    }
]

@app.route("/")
@app.route("/home")
def home():
    
    return render_template("home.html", posts = posts) 

@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #so if the form valid to submit (all length and signs are correct) we can hash the password and do the authentication procedure 
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # "form.password.data" is the password that user has entered and ".decode('utf-8')" is needed to decde from bytes to a regular string
        user = User(username = form.username.data, email = form.email.data, password = hashed_pasword) # getting the data from user into the db, where we get allready hashed password with "password = hashed_pasword"
        #saving the entered dta to the db
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # before we were simply checking the hardcoded data, and now we need to check the database for valid data 
        # firstly the user will be logged in with an email, so we need to write a check for the email in the db:
        user = User.query.filter_by(email = form.email.data).first() # finds the first User by entered email in the id
        if user and bcrypt.check_password_hash(user.password, form.password.data): # so if the user exist and the password the user entered is valid we want to login the user and we also need to import the login user function 
            login_user(user, remember = form.remember.data) # "user" - what we want to login, "remember" - remember me form (boolean) we have created
            next_page = request.args.get('next') # this line
            return redirect(next_page) if next_page else redirect(url_for('home')) # use of ternary conditional 
        else:
            flash("login unsuccessful. Pls check ur email and password", "danger")
    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required #extention knows that we need to be logged in to access this route 
def account():
    return render_template('account.html', title = 'Account')


