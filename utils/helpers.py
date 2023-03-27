from flask import abort, flash, redirect, url_for
from utils.auth import session
from database.db_helpers import get_db_connection

mgr = "manager"
doc = "doctor"
ast = "assistant"

doc_mgm_roles = [mgr]
pat_mgm_roles = [mgr, doc]
ast_mgm_roles = [mgr]
trt_mgm_roles = [mgr, doc]

unauth_error_msg = "Unauthorized access"


def handle_unauth_access():
    flash(unauth_error_msg)
    return redirect(url_for('index'))


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
