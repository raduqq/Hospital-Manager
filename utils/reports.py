import json
from flask import Blueprint, redirect, url_for, flash

from database.db_helpers import get_doctors, get_db_connection
from utils.auth import get_user_role, handle_unauth_access, is_authorized

bp = Blueprint('reports', __name__, url_prefix='/reports')

report_filename = "doctors_report.json"
indent = 4


@bp.route('/doctors', methods=('GET', 'POST'))
def get_doctors_report():
    if is_authorized("manager", get_user_role()):
        report = {}

        doctors = get_doctors()
        query = '''SELECT p.name 
                    FROM patients as p 
                        JOIN assistants AS a
                            ON a.id = p.assistant_id
                        JOIN doctors AS d 
                            ON d.id = a.doctor_id
                    WHERE d.id = ?'''

        conn = get_db_connection()

        for doctor in doctors:
            patients = conn.execute(query, (doctor['id'],)).fetchall()
            patient_array = []

            for patient in patients:
                patient_array.append(patient['name'])

            report[doctor['name']] = patient_array

        report["no_doctors"] = conn.execute("SELECT COUNT(id) FROM doctors").fetchone()[0]
        report["no_assistants"] = conn.execute("SELECT COUNT(id) FROM assistants").fetchone()[0]
        report["no_patients"] = conn.execute("SELECT COUNT(id) FROM patients").fetchone()[0]
        report["no_treatments"] = conn.execute("SELECT COUNT(id) FROM treatments").fetchone()[0]

        conn.close()

        json_obj = json.dumps(report, indent=indent)
        with open(report_filename, "w") as f_out:
            f_out.write(json_obj)

        flash("The report has been successfully generated and locally downloaded as {}".format(
            report_filename))

        return redirect(url_for('index'))

    return handle_unauth_access()
