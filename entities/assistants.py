from flask import Blueprint, request, flash, render_template, abort, redirect, url_for

from database.db_helpers import get_db_connection
from utils.helpers import *

bp = Blueprint('assistants', __name__, url_prefix='/assistants')

def get_assistant(assistant_id):
    conn = get_db_connection()
    assistant = conn.execute('SELECT * FROM assistants WHERE id = ?',
                        (assistant_id,)).fetchone()
    conn.close()

    if assistant is None:
        abort(404)

    return assistant

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        # dropdown cu asistenti

        if not name:
            flash('Name is required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO assistants (name) VALUES (?)',
                            (name,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('assistants/create.html')

@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    assistant = get_assistant(id)

    if request.method == 'POST':
        name = request.form['name']
        # dropdown cu asistenti

        if not name:
            flash('Name is required')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE assistants SET name = ?'
                         ' WHERE id = ?',
                         (name, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('assistants/edit.html', assistant=assistant)

@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized("manager", get_user_role()):
        assistant = get_assistant(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM assistants WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('{} successfully deleted'.format(assistant['name']))
    else:
        flash("Unauthorized access")

    return redirect(url_for('index'))