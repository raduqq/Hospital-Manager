import sqlite3
from os import urandom
from flask import Flask, render_template, request, url_for, flash, redirect, abort
    
app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24).hex()

import auth
app.register_blueprint(auth.bp)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# def get_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?',
#                         (post_id,)).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post

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

# @app.route('/create/', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')
#         elif not content:
#             flash('Content is required!')
#         else:
#             conn = get_db_connection()
#             conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
#                          (title, content))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))

#     return render_template('create.html')

# @app.route('/<int:id>/edit/', methods=('GET', 'POST'))
# def edit(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')

#         elif not content:
#             flash('Content is required!')

#         else:
#             conn = get_db_connection()
#             conn.execute('UPDATE posts SET title = ?, content = ?'
#                          ' WHERE id = ?',
#                          (title, content, id))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))

#     return render_template('edit.html', post=post)

# @app.route('/<int:id>/delete/', methods=('POST',))
# def delete(id):
#     post = get_post(id)
#     conn = get_db_connection()
#     conn.execute('DELETE FROM posts WHERE id = ?', (id,))
#     conn.commit()
#     conn.close()
#     flash('"{}" was successfully deleted!'.format(post['title']))
#     return redirect(url_for('index'))

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

# /doctor/delete
@app.route('/doctors/delete/<int:id>', methods=('POST',))
def delete_doctor(id):
    doctor = get_doctor(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM doctors WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(doctor['name']))
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