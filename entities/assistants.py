from flask import Blueprint, request, flash, render_template, redirect, url_for

from database.db_helpers import get_db_connection
from database.db_helpers import get_assistant_by_id
from utils.auth import get_user_role, handle_unauth_access, is_authorized, ast_mgm_roles

from database.db_helpers import get_doctors
from database.db_helpers import get_patient_by_id
from database.db_helpers import get_treatment_by_id

bp = Blueprint('assistants', __name__, url_prefix='/assistants')


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
        return redirect(url_for('index'))

    return handle_unauth_access()


@bp.route('/apply_treatment/patient/<int:patient_id>', methods=('GET', 'POST'))
def apply_treatment(patient_id):
    if is_authorized("assistant", get_user_role()):
        patient = get_patient_by_id(patient_id)

        treatment = get_treatment_by_id(patient['treatment_id'])
        new_patient_health = patient['health'] + treatment['health_value']
        
        # TODO
        print(type(new_patient_health))

        conn = get_db_connection()
        conn.execute('UPDATE patients SET health = ?'
                     ' WHERE id = ?',
                     (new_patient_health, id))
        conn.commit()
        conn.close()

        flash('Treatment {} successfully applied to patient {}'.format(
            treatment['name'], patient['name']))
        return redirect(url_for('index'))

    return handle_unauth_access()
