from flask import Blueprint, request, flash, render_template, abort, redirect, url_for

from database.db_helpers import get_db_connection
from entities.assistants import get_assistants
from entities.treatments import get_treatments
from utils.helpers import *

bp = Blueprint('patients', __name__, url_prefix='/patients')


def get_patient_by_id(id):
    conn = get_db_connection()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?',
                           (id,)).fetchone()
    conn.close()

    if patient is None:
        abort(404)

    return patient


@bp.route('/create/', methods=('GET', 'POST'))
def create():
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
            conn.execute('INSERT INTO patients (name, assistant_id, treatment_id) VALUES (?, ?, ?)',
                         (name, assistant_id, treatment_id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('patients/create.html', assistants=get_assistants(), treatments=get_treatments())


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
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
            conn.execute('UPDATE patients SET name = ?, assistant_id = ?, treatment_id = ?'
                         ' WHERE id = ?',
                         (name, assistant_id, treatment_id, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('patients/edit.html', patient=patient, assistants=get_assistants(), treatments=get_treatments())


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized("manager", get_user_role()):
        patient = get_patient_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM patients WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('{} successfully deleted'.format(patient['name']))
    else:
        flash("Unauthorized access")

    return redirect(url_for('index'))
