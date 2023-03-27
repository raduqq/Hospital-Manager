from flask import Blueprint, request, flash, render_template, redirect, url_for

from database.db_helpers import get_db_connection
from database.db_helpers import get_patient_by_id
from utils.auth import get_user_role, handle_unauth_access, is_authorized, pat_mgm_roles

from database.db_helpers import get_assistants
from database.db_helpers import get_treatments

bp = Blueprint('patients', __name__, url_prefix='/patients')


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    if is_authorized(pat_mgm_roles, get_user_role()):
        if request.method == 'POST':
            name = request.form['name']
            assistant_id = request.form['assistant_id']
            treatment_id = request.form['treatment_id']

            if not name:
                flash('Name is required')
            elif not assistant_id:
                flash('Assistant is required')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO patients (name, assistant_id, treatment_id) VALUES (?, ?, ?)',
                             (name, assistant_id, treatment_id))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('patients/create.html', assistants=get_assistants(), treatments=get_treatments(), role=get_user_role())

    return handle_unauth_access()


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if is_authorized(pat_mgm_roles, get_user_role()):
        patient = get_patient_by_id(id)

        if request.method == 'POST':
            name = request.form['name']
            assistant_id = request.form['assistant_id']
            treatment_id = request.form['treatment_id']

            if not name:
                flash('Name is required')
            elif not assistant_id:
                flash('Assistant is required')
            elif not treatment_id:
                flash('Treatment is required')
            else:
                conn = get_db_connection()

                if (get_user_role() is "doctor"):
                    conn.execute('UPDATE patients SET name = ?, assistant_id = ?, treatment_id = ?'
                                 ' WHERE id = ?',
                                 (name, assistant_id, treatment_id, id))
                else:
                    conn.execute('UPDATE patients SET name = ?, assistant_id = ?'
                                 ' WHERE id = ?',
                                 (name, assistant_id, id))
                    flash("Treatment has not been modified, as only doctors can attribute it")

                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('patients/edit.html', patient=patient, assistants=get_assistants(), treatments=get_treatments(), role=get_user_role())

    return handle_unauth_access()


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized(pat_mgm_roles, get_user_role()):
        patient = get_patient_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM patients WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        flash('{} successfully deleted'.format(patient['name']))
        return redirect(url_for('index'))

    return handle_unauth_access()
