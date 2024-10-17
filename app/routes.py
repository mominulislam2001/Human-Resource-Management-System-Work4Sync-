from flask import Blueprint, request, jsonify,render_template
from app.models import add_employee,update_employee,delete_employee
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import get_user_by_email, User
from app.access import is_hr,is_employee
from app.models import get_avg_salary_hr_dashboard, get_all_employee_data,\
    get_searched_employee_data,get_all_manager_data,get_employee_info_by_id,get_all_leave_types,\
    apply_for_leave,get_leave_request_by_manager_id,update_status


main = Blueprint('main', __name__)





@main.route('/employee')
@login_required
def employee():
    
    if not is_hr():
        return "Access Denied", 403
    
    
    # Fetch all employees to populate as managers
    managers = get_all_manager_data()  # Assuming this function returns all employees
    
    return render_template('employee_form.html' , managers=managers)




@main.route('/employee_dashboard')
@login_required
def profile():
    
 
    return render_template('employee_dashboard.html')


@main.route('/dashboard')
@login_required
def dashboard():
    
    
    if not is_hr():
        return "Access Denied", 403
    
    avg_salary = get_avg_salary_hr_dashboard()
    
    return render_template('hr_dashboard.html',avg_salary = avg_salary)


@main.route('/search', methods=['GET'])
@login_required
def search_employee_page():
    if not is_hr():
        return "Access Denied", 403
    
    return render_template('search_employee.html')


@main.route('/search_employee', methods=['POST'])
@login_required
def search_employee_route():
    
    if not is_hr():
        return jsonify({'error': 'Access Denied'}), 403
    
    data = request.get_json()
    employee_id = data.get('id')
    employee_email = data.get('email')
    
    # Call the function to get searched employee data
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
        return render_template('employee_dashboard.html')
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
def delete_employee_route(employee_id):
   
    if not is_hr():
        return "Access Denied", 403
    try:
        delete_employee(employee_id)
        return jsonify({'message': 'Employee deleted successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})


@main.route('/get_employee/<int:employee_id>', methods=['GET'])
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
def apply_leave_route():
    
  leave_types = get_all_leave_types()  # Assuming this function returns all employees
    
  return render_template('apply_leave.html',leave_types=leave_types)


@main.route('/apply_for_leave', methods=['POST'])
def apply_leave():
    
    #  todo :  need to validate if employee has leaves in balance
   
    
    data = request.get_json()
    
    try:
        apply_for_leave(data,current_user.id)
        return jsonify({'message': 'Leave Applied Successfully!'})
    
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
@main.route('/leave_requests',methods=['GET'])
def leave_requests_route():
    
    leave_requests = get_leave_request_by_manager_id(current_user.id)
    
    # leave_requests = [
    #     {
    #         "employee_name":"Ayan",
    #         "leave_type":"casual",
    #         "start_date":135,
    #         "end_date":123,
    #         "reason":"vacation",
    #         "status":"Pending"
    #     },
    #      {
    #         "employee_name":"Ayan",
    #         "leave_type":"casual",
    #         "start_date":135,
    #         "end_date":123,
    #         "reason":"vacation",
    #         "status":"Pending"
    #     }
    # ]
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
   
    
@main.route('/employee_dashboard' , methods=['GET'])
@login_required
def employee_dashboard_route():
    user_id = current_user.id
    user_info = get_user_by_id(user_id)  # Fetch user info
    leaves_taken = get_leaves_taken_this_year(user_id)  # Fetch leaves taken this year
    return render_template('employee_dashboard.html')


@main.route('/profile', methods=['GET'])
@login_required
def profile():
    

    return render_template('profile.html', user=user_info, leaves=leaves_taken)
    