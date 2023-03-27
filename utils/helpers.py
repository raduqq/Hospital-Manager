from flask import abort
from utils.auth import session
from database.db_helpers import get_db_connection


def get_user_role():
    if 'user_id' not in session:
        return None

    conn = get_db_connection()
    user_id = session['user_id']
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id,)).fetchone()

    if user is None:
        abort(404)

    return user['role']


def is_authorized(needed_roles, role):
    if role is None:
        return False

    if role in needed_roles:
        return True

    return False
