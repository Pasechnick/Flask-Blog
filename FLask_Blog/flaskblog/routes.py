import os 
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort # abort needed to prevent update the post if the user didn't made this post
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm # PostForm is needed to import all forms we have created  
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all() # grabs all posts, that have been made 
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



def save_picture(form_picture):
    random_hex = secrets.token_hex(8) 
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) 
    
    
    output_size = (125, 125) 
    i = Image.open(form_picture) 
    i.thumbnail(output_size)
    i.save(picture_path) 

    return picture_fn


@app.route("/account", methods =['GET', 'POST']) 
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: 
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !', 'success')
        return redirect(url_for('account')) 
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account',
                            image_file=image_file, form=form)

# route to crate posts
@app.route("/post/new", methods =['GET', 'POST']) 
@login_required
def new_post():
    form = PostForm() # instance of the form to send 
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit() # will add the post to db
        flash("Your Post has been created", "success")
        return redirect(url_for("home"))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


# with flask we can make a variables within our routes
# we want to create an id, where it is a part if the route
# - <int:post_id> where "int" is what we can expect from the variable to be (can be "string" or etc...)
@app.route("/post/new/<int:post_id>") 
def post(post_id):
    # lets fetch this post if it exists - we getting this by id
    post = Post.query.get_or_404(post_id) # we can use a normal ".get" or ".first" to get the id, but ".get_or_404" will find the variable or return a 404 error (page does not exist) 
    return render_template('post.html', title = post.title, post=post)

#update route 
@app.route("/post/new/<int:post_id>/update", methods =['GET', 'POST']) 
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # only the user who wrote this can update this post
    if post.author != current_user:
        abort(403) # 403 is http responce fpr a forbitten route 
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated !', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # then populate the for with below values (old text and title)
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


@app.route("/post/new/<int:post_id>/delete", methods =['POST']) 
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted !', 'success')
    return redirect(url_for('home'))
    



    


