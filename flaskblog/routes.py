from flask import Flask, escape, request, render_template,flash,redirect,url_for
from flaskblog import app,db,bcrypt
from flaskblog.forms import LoginForm, SignupForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user,LoginManager,current_user,logout_user,login_required
from PIL import Image
import os
import secrets

def save_picture(form_picture):
    random_hex = secrets.token_hex(4)
    picture_fn = random_hex+'_'+form_picture.filename
    picture_path = os.path.join(app.root_path,"static/profile_pic",picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn

@app.route('/signup',methods=['GET','POST'])
def signupForm():
    form= SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user = User(username=form.username.data,email=form.email.data,password=hashed_password, image_file=picture_file)
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully! You are able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html',form=form,title='signup')

@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login successful!','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Unsuccessful login! Check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# def make_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title = form.title.data, content = 'form.content.data',user_id=current_user.id)
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('home')) 

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home')) 
    # make_post()
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('account.html',title=current_user.username, image_file=image_file, form=form,posts=posts)




@app.route('/',methods=['GET','POST'])
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    posts = Post.query.all() 
    return render_template('home.html', title='home',form=form, posts=posts)
