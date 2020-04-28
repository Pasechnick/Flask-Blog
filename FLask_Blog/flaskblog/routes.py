from flask import render_template, url_for, flash, redirect
from flaskblog import app
# since we are in the package right now 
# we need to name the package from where it is imported ("flaskblog.forms", "flaskblog.models")
from flaskblog.forms import RegistrationForm, LoginForm 
from flaskblog.models import User, Post
 

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
    form = RegistrationForm()
    if form.validate_on_submit():
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods =['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in !", "success")
            return redirect(url_for('home'))
        else:
            flash("login unsuccessful. Pls check ur username and password", "danger")
    return render_template('login.html', title = 'Login', form = form)
