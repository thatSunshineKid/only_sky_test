# coding: utf-8

from datetime import datetime
import os

from flask import flash, Flask, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.debug import DebuggedApplication
from wtforms import PasswordField, StringField, validators

from app import commands

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}:3306/{}'.format(
    os.getenv('MYSQL_USERNAME', 'web_user'),
    os.getenv('MYSQL_PASSWORD', 'password'),
    os.getenv('MYSQL_HOST', 'db'), os.getenv('MYSQL_DATABASE', 'sample_app'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this is something special'

if app.debug:
    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

db = SQLAlchemy(app)
commands.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) if user_id else None


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.email

    def check_password(self, password):
        return self.password == password


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(
        'Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route("/")
def index():
    pagetitle = "The Bootstrap Blog"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.pub_date.desc()).paginate(page,10,False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url, pagetitle=pagetitle)

@app.route("/archive/<int:month>/<int:year>")
def archive(month,year):
    low = datetime(year, month, 1)
    high = datetime(year, (month + 1), 1)
    pagetitle = "Archive for %s" % (low.strftime("%B %Y"))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.pub_date > low).filter(Post.pub_date < high).order_by(Post.pub_date.desc()).paginate(page,10,False)
    next_url = url_for('archive', month=month, year=year, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('archive', month=month, year=year, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', posts=posts.items, next_url=next_url, prev_url=prev_url, pagetitle=pagetitle )


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        user = User.query.filter_by(email=self.email.data).one_or_none()
        if user:
            password_match = user.check_password(self.password.data)
            if password_match:
                self.user = user
                return True
        self.password.errors.append('Invalid email and/or password specified.')
        return False

class PostForm(FlaskForm):
    title = StringField('Title', validators=[validators.DataRequired()])
    body = StringField('Body', validators=[validators.Length(min=10)])

    def validate(self):
        vf = FlaskForm.validate(self)
        if not vf:
            return False
        else:
            return True

@app.route('/post/create/', methods=['GET', 'POST'])
def createpost():
    pagetitle = "Add a Post"
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, category=Category.query.filter_by(name="General").one_or_none())
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully')
        return redirect(url_for('index'))
    return render_template('postform.html', form=form, pagetitle=pagetitle)


@app.route('/auth/login/', methods=['GET', 'POST'])
def login():
    pagetitle="Login page"
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user)
        flash('Logged in successfully.')
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form, pagetitle=pagetitle)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/account/')
@login_required
def account():
    return render_template('account.html', user=current_user)

@app.route('/about/')
@login_required
def about():
    pagetitle = "About me Page"
    return render_template('about.html', user=current_user, pagetitle=pagetitle)

# @app.route('/posts/')


@app.before_first_request
def initialize_data():
    # just make sure we have some sample data, so we can get started.
    user = User.query.filter_by(email='blogger@sample.com').one_or_none()
    if user is None:
        user = User(email='blogger@sample.com', password='password')
        category = Category(name='General')
        db.session.add(user)
        db.session.add(category)
        db.session.commit()


if __name__ == "__main__":
    app.run()
