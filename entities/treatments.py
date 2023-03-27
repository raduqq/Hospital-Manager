from flask import Blueprint, request, flash, render_template, abort, redirect, url_for

from database.db_helpers import get_db_connection
from utils.helpers import *

bp = Blueprint('treatments', __name__, url_prefix='/treatments')


def get_treatments():
    conn = get_db_connection()
    treatments = conn.execute('SELECT * FROM treatments').fetchall()
    conn.close()

    return treatments


def get_treatment_by_id(id):
    conn = get_db_connection()
    treatment = conn.execute('SELECT * FROM treatments WHERE id = ?',
                             (id,)).fetchone()
    conn.close()

    if treatment is None:
        abort(404)

    return treatment


@bp.route('/create/', methods=('GET', 'POST'))
def create():
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


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    treatment = get_treatment_by_id(id)

    if request.method == 'POST':
        name = request.form['name']
        health_value = request.form['health_value']

        if not name:
            flash('Name is required')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE treatments SET name = ?, health_value = ?'
                         ' WHERE id = ?',
                         (name, health_value, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('treatments/edit.html', treatment=treatment)


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized("manager", get_user_role()):
        treatment = get_treatment_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM treatments WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('{}" successfully deleted'.format(treatment['name']))
    else:
        flash("Unauthorized access")

    return redirect(url_for('index'))