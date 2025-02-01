from flask import Blueprint, request, jsonify,render_template
from app.models import add_employee,update_employee,delete_employee
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import get_user_by_email, User
from app.access import is_hr,is_employee
from app.models import get_avg_salary_hr_dashboard, get_all_employee_data,\
    get_searched_employee_data,get_all_manager_data,get_employee_info_by_id,get_all_leave_types,\
    apply_for_leave,get_leave_request_by_manager_id,update_status,get_employee_all_info_by_id,\
    get_leaves_taken_this_year,insert_payroll_data,fetch_payroll_history
from datetime import datetime

from fpdf import FPDF  # Use fpdf or any other library for PDF generation


main = Blueprint('main', __name__)



@main.route('/employee')
@login_required
def employee():
    
    if not is_hr():
        return "Access Denied", 403
    
    # Fetch all employees to populate as managers
    managers = get_all_manager_data()  # Assuming this function returns all employees
    
    return render_template('employee_form.html' , managers=managers)


@main.route('/dashboard')
@login_required
def dashboard():
    if not is_hr():
        return "Access Denied", 403
    
    # Redirect to the Dash app
    return render_template('hr_dashboard.html',)

@main.route('/search', methods=['GET'])
@login_required
def search_employee_page():
    if not is_hr():
        return "Access Denied", 403
    
    return render_template('search_employee.html')


@main.route('/payroll', methods=['GET'])
@login_required
def payroll_route():
    if not is_hr():
        return "Access Denied", 403
    
    employees = get_all_employee_data()
    
    return render_template('payroll.html',employees=employees)


@main.route('/search_employee', methods=['POST'])
@login_required
def search_employee_route():
    
    if not is_hr():
        return jsonify({'error': 'Access Denied'}), 403
    
    data = request.get_json()
    employee_id = data.get('id')
    employee_email = data.get('email')
    
    
    employee_data = get_searched_employee_data(employee_id=employee_id, employee_email=employee_email)
    
    if not employee_data:
        return jsonify({'error': 'Employee not found'}), 404
    
    return jsonify(employee_data)



@main.route('/view')
@login_required
def view_employees():
    
    if not is_hr():
        return "Access Denied", 403
    
    employees_data = get_all_employee_data()
    
    return render_template('view_employees.html',employees = employees_data)


@main.route('/')
@login_required
def index():
    
    
    if is_hr():
        return dashboard()
    elif is_employee():
        return render_template('employee_dashboard.html',employee=None)
    else:
        return "Access Denied", 403




@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Fetch the user details from the DB
        user_data = get_user_by_email(email)
       
        if user_data and user_data[3] == password:  # Check the password (you should hash passwords)
            user = User(id=user_data[0], email=user_data[1], role=user_data[2])
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
    
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/add_employee', methods=['POST'])
@login_required
def add_employee_route():
    if not is_hr():
        return "Access Denied", 403
    
    data = request.get_json()
    try:
        add_employee(data)
        return jsonify({'message': 'Employee added successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@main.route('/update_employee/<int:employee_id>', methods=['PUT'])
@login_required
def update_employee_route(employee_id):
    if not is_hr():
        return "Access Denied", 403
    
    data = request.get_json()
    try:
        update_employee(employee_id, data)
        return jsonify({'message': 'Employee updated successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})


@main.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
@login_required
def delete_employee_route(employee_id):
   
    if not is_hr():
        return "Access Denied", 403
    try:
        delete_employee(employee_id)
        return jsonify({'message': 'Employee deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})


@main.route('/get_employee/<int:employee_id>', methods=['GET'])
@login_required
def get_employee(employee_id):
    
    employee_info = get_employee_info_by_id(employee_id)
    
    if employee_info:
        # Convert tuple to dictionary for easier access
        employee_data = {
            'id': employee_info[0],
            'first_name': employee_info[1],
            'last_name': employee_info[2],
            'salary': employee_info[3],
            'department': employee_info[4],
            'position': employee_info[5],
            'gender': employee_info[6],
            'role': employee_info[7],
            'hire_date': employee_info[8].isoformat() if employee_info[8] else None,
            'end_date': employee_info[9].isoformat() if employee_info[9] else None,
            'email': employee_info[10],
            'phone': employee_info[11],
            'manager_id': employee_info[12],
            'address': employee_info[13]
        }
        return jsonify(employee_data)
    else:
        return jsonify({'error': 'Employee not found'}), 404
    
    


@main.route('/apply_leave', methods=['GET'])
@login_required
def apply_leave_route():
    
  leave_types = get_all_leave_types()  # Assuming this function returns all employees
    
  return render_template('apply_leave.html',leave_types=leave_types)


@main.route('/apply_for_leave', methods=['POST'])
@login_required
def apply_leave():
    
    #  todo :  need to validate if employee has leaves in balance
   
    
    data = request.get_json()
    
    try:
        apply_for_leave(data,current_user.id)
        return jsonify({'message': 'Leave Applied Successfully!'})
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@main.route('/leave_requests',methods=['GET'])
@login_required
def leave_requests_route():
    
    leave_requests = get_leave_request_by_manager_id(current_user.id)
   
    return render_template('leave_requests.html',leave_requests=leave_requests)



@main.route('/update_leave_status/<int:leave_id>', methods=['PUT'])
@login_required
def update_leave_status(leave_id):
      
    data = request.get_json()
    new_status = data.get('status')
    
    try:
        update_status(new_status,leave_id,current_user.id)
        return jsonify({'message': 'Leave Status Updated'})
    
    except Exception as e:
        return jsonify({'error': str(e)})
   
    
@main.route('/employee_dashboard', methods=['GET'])
@login_required
def employee_dashboard_route():
    # Dummy employee information
    employee_info = {
        'name': 'Mominul Islam',
        'email': 'ayan@gmail.com',
        'position': 'HR',
        'department': 'Data Analytics',
        'joining_date': '2021-06-15'
    }

    # Dummy leave balance data
    leave_balances = [
        {'leave_type': 'Annual Leave', 'total_leaves': 20, 'used_leaves': 5, 'remaining_leaves': 15},
        {'leave_type': 'Sick Leave', 'total_leaves': 10, 'used_leaves': 2, 'remaining_leaves': 8},
        {'leave_type': 'Casual Leave', 'total_leaves': 12, 'used_leaves': 4, 'remaining_leaves': 8}
    ]

    return render_template('employee_dashboard.html', employee=employee_info, leave_balances=leave_balances)






from flask import jsonify, request, send_from_directory
from datetime import datetime
import os

@main.route('/process_payroll', methods=['POST'])
def process_payroll():
    employee_id = request.form['employee_id']
    salary = float(request.form['salary'])
    deductions = float(request.form.get('deductions', 0))
    bonuses = float(request.form.get('bonuses', 0))

    # Calculate total pay
    total_pay = salary - deductions + bonuses
    
    print(total_pay)
    employee = insert_payroll_data(employee_id, salary, deductions, bonuses, total_pay)
    
    if not employee:
        return jsonify(success=False, message='Employee not found.')

    employee_first_name = employee[0]
    employee_last_name = employee[1]
    position = employee[2]
    
    # Get the current month as a string
    month = datetime.now().strftime('%B')  # e.g., "November"
    
    # Generate PDF slip
    slip_path = f'/slips/{employee_first_name}_{employee_last_name}_{month}_payroll_slip.pdf'
    file_name = f'{employee_first_name}_{employee_last_name}_{month}_payroll_slip.pdf'
    generate_pdf_slip(employee_first_name + " " + employee_last_name, position, month, salary, deductions, bonuses, total_pay)
    
    # Return JSON response with all necessary data including slip URL
    return jsonify(success=True,
                   employee_name=f"{employee_first_name} {employee_last_name}",
                   position=position,
                   month=month,
                   salary=salary,
                   deductions=deductions,
                   bonuses=bonuses,
                   total_pay=total_pay,
                   slip_url=slip_path,
                   file_name=file_name)  # Include slip URL in response



from flask import send_from_directory

@main.route('/slips/<path:filename>', methods=['GET'])
def download_slip(filename):
    return send_from_directory('slips', filename)


def generate_pdf_slip(employee_name, position, month, salary, deductions, bonuses, total_pay):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Payroll Slip', ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f'Employee Name: {employee_name}', ln=True)
    pdf.cell(0, 10, f'Position: {position}', ln=True)
    pdf.cell(0, 10, f'Month: {month}', ln=True)
    
    pdf.cell(0, 10, f'Base Salary: ${salary:.2f}', ln=True)
    pdf.cell(0, 10, f'Deductions: ${deductions:.2f}', ln=True)
    pdf.cell(0, 10, f'Bonuses: ${bonuses:.2f}', ln=True)
    pdf.cell(0, 10, f'Total Pay: ${total_pay:.2f}', ln=True)

    # Save PDF to a file
    slip_path = f'slips/{employee_name.replace(" ", "_")}_{month}_payroll_slip.pdf'
    pdf.output(slip_path)

    return slip_path 


@main.route('/download/<file_name>')
def download_file(file_name):
    directory = "D:/Projects/HRM_app/slips"  # Adjust to your actual directory
    return send_from_directory(directory, file_name, as_attachment=True)






@main.route('/payroll_history', methods=['GET', 'POST'])
def payroll_history():
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        if employee_id:
            payroll_history = fetch_payroll_history(employee_id)
            employees = get_all_employee_data()
            return render_template('payroll_history.html', employees=employees, payroll_history=payroll_history)
    
    # For GET request, just render the page with the list of employees
    employees = get_all_employee_data()
    return render_template('payroll_history.html', employees=employees, payroll_history=None)
