from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "tt_group_secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tt_group.db'
db = SQLAlchemy(app)

# This creates the Database Table
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)

@app.route('/')
def index():
    records = Attendance.query.order_by(Attendance.id.desc()).all()
    return render_template('index.html', records=records)

@app.route('/checkin', methods=['POST'])
def checkin():
    emp_id = request.form.get('employee_id').strip().upper()
    # Prevent double check-in
    active_session = Attendance.query.filter_by(employee_id=emp_id, check_out=None).first()
    if active_session:
        flash(f"Employee {emp_id} is already checked in!")
    else:
        new_record = Attendance(employee_id=emp_id, check_in=datetime.now())
        db.session.add(new_record)
        db.session.commit()
    return redirect('/')

@app.route('/checkout', methods=['POST'])
def checkout():
    emp_id = request.form.get('employee_id').strip().upper()
    record = Attendance.query.filter_by(employee_id=emp_id, check_out=None).first()
    if record:
        record.check_out = datetime.now()
        db.session.commit()
    else:
        flash(f"No active session found for {emp_id}")
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)