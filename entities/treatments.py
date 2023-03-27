from flask import Blueprint, request, flash, render_template, redirect, url_for

from database.db_helpers import get_db_connection
from database.db_helpers import get_treatment_by_id
from utils.auth import get_user_role, handle_unauth_access, is_authorized, trt_mgm_roles

bp = Blueprint('treatments', __name__, url_prefix='/treatments')


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    if is_authorized(trt_mgm_roles, get_user_role()):
        if request.method == 'POST':
            name = request.form['name']
            health_value = request.form['health_value']

            if not name:
                flash('Name is required')
            elif not health_value:
                flash('Health value is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO treatments (name, health_value) VALUES (?, ?)',
                             (name, health_value))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('treatments/create.html')

    return handle_unauth_access()


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if is_authorized(trt_mgm_roles, get_user_role()):
        treatment = get_treatment_by_id(id)

        if request.method == 'POST':
            name = request.form['name']
            health_value = request.form['health_value']

            if not name:
                flash('Name is required')
            if not health_value:
                flash('Health value is required')
            else:
                conn = get_db_connection()
                conn.execute('UPDATE treatments SET name = ?, health_value = ?'
                             ' WHERE id = ?',
                             (name, health_value, id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('treatments/edit.html', treatment=treatment)

    return handle_unauth_access()


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized(trt_mgm_roles, get_user_role()):
        treatment = get_treatment_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM treatments WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        flash('{}" successfully deleted'.format(treatment['name']))
        return redirect(url_for('index'))

    return handle_unauth_access()

