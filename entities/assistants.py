from flask import Blueprint, request, flash, render_template, abort, redirect, url_for

from database.db_helpers import get_db_connection
from entities.doctors import get_doctors
from utils.helpers import *

bp = Blueprint('assistants', __name__, url_prefix='/assistants')


def get_assistants():
    conn = get_db_connection()
    assistants = conn.execute('SELECT * FROM assistants').fetchall()
    conn.close()

    return assistants


def get_assistant_by_id(id):
    conn = get_db_connection()
    assistant = conn.execute('SELECT * FROM assistants WHERE id = ?',
                             (id,)).fetchone()
    conn.close()

    if assistant is None:
        abort(404)

    return assistant


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    if is_authorized(ast_mgm_roles, get_user_role()):
        if request.method == 'POST':
            name = request.form['name']
            doctor_id = request.form['doctor_id']

            if not name:
                flash('Name is required')
            elif not doctor_id:
                flash('Doctor is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO assistants (name, doctor_id) VALUES (?, ?)',
                             (name, doctor_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('assistants/create.html', doctors=get_doctors())

    return handle_unauth_access()


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if is_authorized(ast_mgm_roles, get_user_role()):
        assistant = get_assistant_by_id(id)

        if request.method == 'POST':
            name = request.form['name']
            doctor_id = request.form['doctor_id']

            if not name:
                flash('Name is required')
            elif not doctor_id:
                flash('Doctor is required')
            else:
                conn = get_db_connection()
                conn.execute('UPDATE assistants SET name = ?, doctor_id = ?'
                             ' WHERE id = ?',
                             (name, doctor_id, id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('assistants/edit.html', assistant=assistant, doctors=get_doctors())

    return handle_unauth_access()


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized(ast_mgm_roles, get_user_role()):
        assistant = get_assistant_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM assistants WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('{} successfully deleted'.format(assistant['name']))

    return handle_unauth_access()
