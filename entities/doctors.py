from flask import Blueprint, request, flash, render_template, redirect, url_for

from database.db_helpers import get_db_connection
from database.db_helpers import get_doctor_by_id
from utils.auth import get_user_role, handle_unauth_access, is_authorized, doc_mgm_roles

bp = Blueprint('doctors', __name__, url_prefix='/doctors')


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    if is_authorized(doc_mgm_roles, get_user_role()):
        if request.method == 'POST':
            name = request.form['name']

            if not name:
                flash('Name is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO doctors (name) VALUES (?)',
                             (name,))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('doctors/create.html')

    return handle_unauth_access()


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if is_authorized(doc_mgm_roles, get_user_role()):
        doctor = get_doctor_by_id(id)

        if request.method == 'POST':
            name = request.form['name']

            if not name:
                flash('Name is required')

            else:
                conn = get_db_connection()
                conn.execute('UPDATE doctors SET name = ?'
                             ' WHERE id = ?',
                             (name, id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('doctors/edit.html', doctor=doctor)

    return handle_unauth_access()


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized(doc_mgm_roles, get_user_role()):
        doctor = get_doctor_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM doctors WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        flash('{} successfully deleted'.format(doctor['name']))
        return redirect(url_for('index'))

    return handle_unauth_access()
