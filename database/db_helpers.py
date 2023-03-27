import sqlite3
import click

from flask import abort, current_app, g

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    # Clear the existing data and create new tables
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


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

def get_doctor_by_id(id):
    conn = get_db_connection()
    doctor = conn.execute('SELECT * FROM doctors WHERE id = ?',
                          (id,)).fetchone()
    conn.close()

    if doctor is None:
        abort(404)

    return doctor

def get_doctors():
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()

    return doctors

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

def get_patient_by_id(id):
    conn = get_db_connection()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?',
                           (id,)).fetchone()
    conn.close()

    if patient is None:
        abort(404)

    return patient


