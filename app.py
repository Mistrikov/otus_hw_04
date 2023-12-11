from db.api import create_user, add_post, update_post, add_comment, get_user_by_id, get_user_by_login, get_users, get_post_by_id, isExistUser
from db.models import db, User, Comment, Post
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin,  login_required, login_user, current_user, logout_user
from flask_wtf import csrf
from flask_migrate import Migrate
from flask import session
from pathlib import Path
from os import getenv
from forms import LoginForm, RegForm, EditPost
from flask_ckeditor import CKEditor
from werkzeug.datastructures import MultiDict

# пути для папок
template_dir = Path(__file__).parent / 'templates/'
static_dir = Path(__file__).parent / 'static/'

# загрузка .Env ключей
secret_key = getenv('SECRET_KEY', 'no_key_(')

#DEFAULT_DB_URI = f"sqlite:///{Path(__file__).parent}/blog.sqlite3"
DEFAULT_DB_URI = 'postgresql+psycopg2://user:user123@pg:5432/blog'

database_uri = getenv('SQLALCHEMY_DATABASE_URI', DEFAULT_DB_URI)
print('database_uri', database_uri)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SECRET_KEY'] = secret_key # шифрование данных
#app.register_blueprint(contacts)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
ckeditor = CKEditor(app)

@app.cli.command("create-db")
def create_db():
    db.drop_all()
    db.create_all()

@app.cli.command("add-demo")
def add_demo():
    maintemp(db)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        #return User.get(user_id)
        return get_user_by_id(db.session, user_id=user_id)
    return None

@app.route('/')
def index():
    PostMessages = db.session.query(Post, User).join(User, User.id == Post.author, isouter=True).all()
    return render_template('index.html', PostMessages=PostMessages, message='')

@app.route('/myposts')
def myposts():
    PostMessages = db.session.query(Post).where(Post.author == current_user.id).all()
    return render_template('myposts.html', PostMessages=PostMessages, message='')

@app.route('/aboutus/')
def aboutus():
    return render_template('about.html')

@app.route('/post/<int:post_id>/')
def post_by_id(post_id):
    PostMessage = Post.query.get_or_404(post_id)
    if PostMessage is not None:
        author = User.query.get(PostMessage.author)
    return render_template('post.html', PostMessage=PostMessage, author=author)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(User.login == form.loginedt.data).first()
            #print('user', user)
            if user and user.check_password(form.passwdedt.data):
                login_user(user)
                return redirect('/myposts')
            return render_template('login.html', form=form, message='Неверный логин или пароль')
        return render_template('login.html', form=form, message='')
    return render_template('lk.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        form = RegForm()
        if form.validate_on_submit():
            if form.passwdedt.data == form.passwd2edt.data:
                #print('check', isExistUser(db.session, login=form.loginedt.data, email=form.emailedt.data))
                if not isExistUser(db.session, login=form.loginedt.data, email=form.emailedt.data):
                    user = create_user(db.session, login=form.loginedt.data, password=form.passwdedt.data, username=form.usernameedt.data, email=form.emailedt.data)
                    login_user(user)
                    return redirect('/myposts') 
                return render_template('register.html', form=form, message='Пользователь с таким логином или почтой уже существует')     
            return render_template('register.html', form=form)
        return render_template('register.html', form=form)
    return redirect('/lk')

@app.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect('/')

@app.route('/lk')
@login_required
def lk():
    return render_template('lk.html')

@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def newpost():
    if current_user.is_authenticated:
        form = EditPost()
        if form.validate_on_submit():
            add_post(db.session, author=current_user.id, title=form.titleedt.data, content=form.contentedt.data, tags=form.tagsedt.data)
            return redirect('/myposts')
        return render_template('post-edit.html', form=form, PostMessage=None)
    return redirect('/')

@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    if current_user.is_authenticated:
        PostMessage = get_post_by_id(db.session, post_id)
        form = EditPost()
        if form.validate_on_submit():
            update_post(db.session, id=PostMessage.id, author=current_user.id, title=form.titleedt.data, content=form.contentedt.data, tags=form.tagsedt.data)
            return redirect('/myposts')
        message = ''
        return render_template('post-edit.html', form=form, PostMessage=PostMessage, message=message)
    return redirect('/')

def maintemp(db):
        # создание Демо-данных
        session=  db.session
        user1 = create_user(session, login='user1', password='1234', username='John', email='john@ya.ru').id
        user2 = create_user(session, login='user2', password='1234', username='Bob', email='bob@ya.ru').id
        post1 = add_post(session, title='Треугольник', content='<img src="/static/images/o-treug.png"><br>Треугольник - это геометрическая фигура у которой три стороны и три угла', tags='треугольник', author=user1).id
        add_post(session, title='Остроугольный треугольник', content='<img src="/static/images/o-treug.png"><br>Треугольник у которого все угля меньше 90 градусов называется остроугольным', tags='треугольник остроугольный', author=user1)
        add_post(session, title='Прямоугольный треугольник', content='<img src="/static/images/p-treug.png"><br>Треугольник у которого один из углов равен 90 градусам называется прямоугольным', tags='треугольник прямоугольный', author=user1)
        add_post(session, title='Тупоугольный треугольник', content='<img src="/static/images/t-treug.png"><br>Треугольник у которого один из углов больше 90 градусов называется тупоугольным', tags='треугольник тупоугольный', author=user1)
        add_comment(session, author=user2, post_id=post1, content='Классно! А какие треугольники бывают?')
        add_comment(session, author=user2, post_id=post1, content='Расскажите подробнее, пожаааалуйста :)')
        post5 = add_post(session, title='Равносторонний треугольник', content='<img src="/static/images/r-treug.png"><br>Я тоже хочу добавить! Еще бывают равносторонними! Это такие треугольники, в которых все стороны равной длинны', tags='треугольник равносторонний', author=user2).id
        add_comment(session, author=user1, post_id=post5, content='Спасибо :)')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=5000)
    #app.run(host='10.8.0.9', debug = True, port=5000)