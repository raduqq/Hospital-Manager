import sqlite3
from os import urandom
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from auth import session

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24).hex()
app.config['DATABASE'] = "database.db"

import auth
app.register_blueprint(auth.bp)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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

def get_doctor(doctor_id):
    conn = get_db_connection()
    doctor = conn.execute('SELECT * FROM doctors WHERE id = ?',
                        (doctor_id,)).fetchone()
    conn.close()

    if doctor is None:
        abort(404)

    return doctor

@app.route('/')
def index():
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()
    return render_template('index.html', doctors=doctors)

# /doctor/create
@app.route('/doctors/create/', methods=('GET', 'POST'))
def create_doctor():
    if request.method == 'POST':
        name = request.form['name']
        # dropdown cu asistenti

        if not name:
            flash('Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO doctors (name) VALUES (?)',
                         (name,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create-doctor.html')

# /doctor/edit
@app.route('/doctors/edit/<int:id>', methods=('GET', 'POST'))
def edit_doctor(id):
    doctor = get_doctor(id)

    if request.method == 'POST':
        name = request.form['name']
        # dropdown cu asistenti

        if not name:
            flash('Name is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE doctors SET name = ?'
                         ' WHERE id = ?',
                         (name, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit-doctor.html', doctor=doctor)

def is_authorized(needed_roles, role):
    if role is None:
        return False

    if role in needed_roles:
        return True
    
    return False

# /doctor/delete
@app.route('/doctors/delete/<int:id>', methods=('GET', 'POST'))
def delete_doctor(id):
    if is_authorized("manager", get_user_role()):
        doctor = get_doctor(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM doctors WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash('"{}" was successfully deleted!'.format(doctor['name']))
    else:
        flash("N-ai dreptu, ba")

    return redirect(url_for('index'))

# /assistant/create
# /assistant/edit
# /assistant/delete

# /patient/create
# /patient/edit
# /patient/delete

# /treatment/create
# /treatment/edit
# /treatment/delete