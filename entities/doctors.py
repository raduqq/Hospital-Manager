from flask import Blueprint, request, flash, render_template, abort, redirect, url_for

from database.db_helpers import get_db_connection
from utils.helpers import *

bp = Blueprint('doctors', __name__, url_prefix='/doctors')


def get_doctors():
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()

    return doctors


def get_doctor_by_id(id):
    conn = get_db_connection()
    doctor = conn.execute('SELECT * FROM doctors WHERE id = ?',
                          (id,)).fetchone()
    conn.close()

    if doctor is None:
        abort(404)

    return doctor


@bp.route('/create/', methods=('GET', 'POST'))
def create():
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


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
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


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    if is_authorized("manager", get_user_role()):
        doctor = get_doctor_by_id(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM doctors WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('{}" successfully deleted'.format(doctor['name']))
    else:
        flash("Unauthorized access")

    return redirect(url_for('index'))
