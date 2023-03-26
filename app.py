from os import urandom
from flask import Flask, render_template

from database.db_helpers import get_db_connection
import utils.auth as auth
import entities.doctors as doctors

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24).hex()
app.config['DATABASE'] = "database/database.db"

app.register_blueprint(auth.bp)
app.register_blueprint(doctors.bp)

@app.route('/')
def index():
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()
    return render_template('index.html', doctors=doctors)