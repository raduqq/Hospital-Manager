import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from database.db_helpers import get_db, get_db_connection

mgr = "manager"
doc = "doctor"
ast = "assistant"

doc_mgm_roles = [mgr]
pat_mgm_roles = [mgr, doc]
ast_mgm_roles = [mgr]
trt_mgm_roles = [mgr, doc]

unauth_error_msg = "Unauthorized access"

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        # get role
        role = ""

        if "mgr" in username:
            role = "manager"
        elif "doc" in username:
            role = "doctor"
        elif "ast" in username:
            role = "assistant"
        else:
            error = 'No assignable role available'

        if error is None:
            try:

                db.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), role),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

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

def handle_unauth_access():
    flash(unauth_error_msg)
    return redirect(url_for('index'))


