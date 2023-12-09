from db.api import create_user, add_post, add_comment, get_user_by_id, get_user_by_login, get_users, get_posts_by_id
from db.models import db, User, Comment, Post
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from pathlib import Path
from os import getenv

# пути для папок
template_dir = Path(__file__).parent / 'templates/'
static_dir = Path(__file__).parent / 'static/'

# загрузка .Env ключей
secret_key = getenv('SECRET_KEY', 'no_key_(')

#DEFAULT_DB_URI = f"sqlite:///{Path(__file__).parent}/blog.sqlite3"
DEFAULT_DB_URI = 'postgresql+psycopg2://user:user123@localhost:5432/blog'

database_uri = getenv('SQLALCHEMY_DATABASE_URI', DEFAULT_DB_URI)
print('database_uri', database_uri)
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SECRET_KEY'] = secret_key # шифрование данных
#app.register_blueprint(contacts)
db.init_app(app)
migrate = Migrate(app, db)

@app.cli.command("create-db")
def create_db():
    #db.drop_all()
    db.create_all()
    maintemp(db)


@app.route('/')
def index():
    PostMessages = db.session.query(Post, User).join(User, User.id == Post.author, isouter=True).all()
    return render_template('index.html', PostMessages=PostMessages)

@app.route('/aboutus/')
def aboutus():
    return render_template('about.html')

@app.route('/post/<int:post_id>/')
def post_by_id(post_id):
    PostMessage = Post.query.get_or_404(post_id)
    if PostMessage is not None:
        user = User.query.get(PostMessage.author)
    return render_template('post.html', PostMessage=PostMessage, user=user)

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
    #app.run(host='10.8.0.9', port=5000)
    app.run(host='0.0.0.0', debug = True, port=5000)
    #app.run(host='10.8.0.9')