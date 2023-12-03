import pytest, sqlite3

@pytest.fixture
def session(): # 1
    connection = sqlite3.connect(':memory:')
    db_session = connection.cursor()
    yield db_session
    connection.close()


@pytest.fixture
def setup_db(session): # 2
    session.execute('CREATE TABLE users (\
        id INTEGER NOT NULL, \
        login VARCHAR(32) NOT NULL, \
        password VARCHAR(32) NOT NULL, \
        username VARCHAR(32) NOT NULL, \
        email VARCHAR, \
        PRIMARY KEY (id), \
        UNIQUE (login), \
        UNIQUE (email)\
)')
    session.execute('INSERT INTO users (login, password, username, email) VALUES ("login1", "1234", "username1", "login1@login.ru")')
    session.connection.commit()

'''@pytest.fixture
def cache(session): # 1
    return CacheService(session)'''