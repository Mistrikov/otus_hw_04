import pytest, sqlite3
from db.api import get_user_by_id, get_user_by_login

@pytest.mark.usefixtures("setup_db") # 1
def test_get_user_by_login(session):
    existing = get_user_by_login(session, user_login = 'login1')
    assert existing