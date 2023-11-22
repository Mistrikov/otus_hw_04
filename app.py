from db.api import create_user, add_post, add_comment, get_user_by_id, get_user_by_login, get_users, get_posts_by_id
from db.config import engine

from sqlalchemy.orm import (
    Session,  
)

with Session(engine) as session:
        user1 = create_user(session, login='user1', password='1234', username='John', email='john@ya.ru').id
        user2 = create_user(session, login='user2', password='1234', username='Bob', email='bob@ya.ru').id
        post1 = add_post(session, title='Треугольник', content='Треугольник - это геометрическая фигура у которой три стороны и три угла', tags='треугольник', author=user1).id
        add_post(session, title='Остроугольный треугольник', content='Треугольник у которого все угля меньше 90 градусов называется остроугольным', tags='треугольник остроугольный', author=user1)
        add_post(session, title='Прямоугольный треугольник', content='Треугольник у которого один из углов равен 90 градусам называется прямоугольным', tags='треугольник прямоугольный', author=user1)
        add_post(session, title='Тупоугольный треугольник', content='Треугольник у которого один из углов больше 90 градусов называется тупоугольным', tags='треугольник тупоугольный', author=user1)
        add_comment(session, author=user2, post_id=post1, content='Классно! А какие треугольники бывают?')
        add_comment(session, author=user2, post_id=post1, content='Расскажите подробнее, пожаааалуйста :)')
        post5 = add_post(session, title='Равносторонний треугольник', content='Я тоже хочу добавить! Еще бывают равносторонними! Это такие треугольники, в которых все стороны равной длинны', tags='треугольник равносторонний', author=user2).id
        add_comment(session, author=user1, post_id=post5, content='Спасибо :)')
        # Поиск пользователя по id
        #user = get_user_by_id(session, user_id=1)
        #print('Пользователь не найден' if user is None else user.username)
        
        # Поиск пользователя по login
        #user = get_user_by_login(session, user_login='user2')
        #print(user)
        #print('Пользователь не найден' if user is None else user.username)
        
        # Список всех пользователей
        #users = get_users(session)
        #for user in users:
        #    print(user.username)
        
        # список постов одного пользователя
        posts = get_posts_by_id(session, author_id=1)
        for post in posts:
            print(post.title)
        