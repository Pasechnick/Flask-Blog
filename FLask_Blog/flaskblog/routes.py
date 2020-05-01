import os # need to grab the file extention of the uploaded image and saves it do db with this extention (image.jpg, image.png, ect..)
import secrets # we need in order to get randomize picture name when we upload a new pic
from PIL import Image # this class is installed with Pillow package (pip3 install Pillow) so we can autoresize big pictures to prevent the site from loading big files
from flask import render_template, url_for, flash, redirect, request 
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # we need UpdateAccountForm so we can use 
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username = form.username.data, email = form.email.data, password = hashed_pasword)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created ! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("login unsuccessful. Pls check ur email and password", "danger")
    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# logic for uploading a new picture as avatar 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # saves picture we upload with random hex token 8 bytes
    _, f_ext = os.path.splitext(form_picture.filename) # we need the file extention at the end of the filename. we do not need to grab the file name so we can use underscore "_" to through away a variable name 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #full path to the package directory
    
    # resizing picture (the upload image might be too big, so the page will load slowly in some cases), so we can change it to our needed size
    output_size = (125, 125) # sets the size...
    i = Image.open(form_picture) #
    i.thumbnail(output_size)
    i.save(picture_path) # saves resized pic to it's path

    return picture_fn


@app.route("/account", methods =['GET', 'POST']) 
@login_required
def account():
    # creates an instance of that Update form 
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: 
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !', 'success')
        return redirect(url_for('account')) # we need to redirect right after data submitted, cuz of get\post method
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # it grabs the image in the user model (models.py) where we hardcoded that the default user image is the "default.jpg"
    return render_template('account.html', title = 'Account',
                            image_file=image_file, form=form)


    


