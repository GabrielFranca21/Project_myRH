from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import config
from forms import EmployeeForm

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def get_db_connection():
    return pymysql.connect(
        host=config.DATABASE['host'],
        user=config.DATABASE['user'],
        password=config.DATABASE['password'],
        db=config.DATABASE['db']
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        position = form.position.data
        department = form.department.data
        hiring_date = form.hiring_date.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        skills = form.skills.data

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO employees (full_name, position, department, hiring_date, email, phone, address, skills) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (full_name, position, department, hiring_date, email, phone, address, skills))
        connection.commit()
        connection.close()

        flash("Employee added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add_employee.html', form=form)

@app.route('/employees')
def employees():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    connection.close()

    return render_template('employees.html', employees=employees)

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()

    if employee is None:
        flash("Employee not found.", "danger")
        return redirect(url_for('index'))

    form = EmployeeForm(obj=employee)

    if form.validate_on_submit():
        full_name = form.full_name.data
        position = form.position.data
        department = form.department.data
        hiring_date = form.hiring_date.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        skills = form.skills.data

        cursor.execute("UPDATE employees SET full_name=%s, position=%s, department=%s, hiring_date=%s, email=%s, phone=%s, address=%s, skills=%s WHERE id=%s", (full_name, position, department, hiring_date, email, phone, address, skills, id))
        connection.commit()
        connection.close()

        flash("Employee updated successfully!", "success")
        return redirect(url_for('employees'))

    return render_template('edit_employee.html', form=form, employee=employee)

@app.route('/delete_employee/<int:id>')
def delete_employee(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    connection.commit()
    connection.close()

    flash("Employee deleted successfully!", "success")
    return redirect(url_for('employees'))

if __name__ == '__main__':
    app.run(debug=True)
