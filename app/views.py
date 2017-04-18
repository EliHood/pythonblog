from flask import render_template, flash, redirect, url_for, request, session, escape, abort, g
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db, bcrypt, slugify, os, HTTPBasicAuth, jsonify, JWT
from .models import User, Post
from datetime import datetime

auth = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

app.secret_key = 'secetttttt'


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def index():
    author = str(g.user)
    return render_template('index.html', title="home", author=author)
    
@app.route('/posts/<slug>/edit', methods=['GET','POST'])
def edit(slug, body=None):
    link = db.session.query(Post).filter_by(slug=slug).first()
    
    if request.method == 'GET':
        return render_template("edit.html", postq=link, post=link)
    update = db.session.query(Post).filter_by(slug=slug).first()
    update.title = request.form['title']
    update.body = request.form['body']
    update.slug = slugify(request.form['title'])
    db.session.add(update)
    db.session.commit()
    flash('Your post has been updated.')
    return redirect (url_for('index'))

@app.route('/posts/<slug>')
@login_required
def show(slug):


    post = db.session.query(Post).filter_by(slug = slug).first()
    title = post.title
    slug = post.slug
  
    if post:
        return render_template("post.html", post=post, title=title, slug=slug)

    abort(404)

@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts, title="Posts")
 
@app.route('/posts/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('index'))
        
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))
    
    
@app.route('/posts/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'GET':
        return render_template('create_post.html', title="Create Post")
    
    else:
        title = request.form['title']
        body = request.form['body']
        slug = slugify(title).lower()
        author = g.user
        post = Post(title=title, body=body, slug=slug, author=author)
        db.session.add(post)
        db.session.commit()
        return redirect (url_for('posts'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title="Register")
    username = request.form['username']
    password = request.form['password']
    user = User(request.form['username'], request.form['password'])
    storeduser = User.query.filter_by(username=username).first()
    if storeduser is not None and storeduser.username == request.form['username']:
        return 'User already Exist!'
        return redirect(url_for('index'))
    
    else:
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        flash('User successfully registered')
        return redirect (url_for('index'))
  
    
@app.route('/login', methods=['GET','POST'] )
def login():
    if g.user.is_authenticated:
        return redirect(url_for('index'))
    
    else:
        if request.method == 'GET':
            return render_template('login.html')
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            session['logged_in'] = True
            flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('index'))
        
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
            
            
@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully')
    session.pop('logged_in', None)
    return redirect(url_for('index')) 
    
    


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@app.route('/default')
def default_jsonencoder():
    now = datetime.now()
    return jsonify({'now': now})


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))

     
    
    posts = user.posts.all()
    
    return render_template('user.html',
                           user=user,
                           posts=posts)