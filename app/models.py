from datetime import datetime
from flask_login import UserMixin
from flask import jsonify


class User(UserMixin):
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

def get_user_by_id(user_id):
    from app import mysql  # Move import inside the function to avoid circular import
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,email,role FROM employees WHERE id=%s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(id=user[0], email=user[1], role=user[2])
    return None

def get_user_by_email(email):
    from app import mysql  # Move import inside the function
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,email,role,password FROM employees WHERE email=%s', (email,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return user  # Return tuple (id,email,role,password,)
    return None

def add_employee(data):
    from app import mysql  # Move import inside the function
    
    
   
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    phone = data.get('phone')
    department = data['department']
    position = data['position']
    gender  = data["gender"]
    role = data["role"]
    manager_id = data["manager_id"]
    address = data["address"]
    hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
    
    salary = data['salary']

    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO employees (first_name, last_name, email, phone, department, position, hire_date,gender,role, manager_id,salary,address)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s)
    ''', (first_name, last_name, email, phone, department, position, hire_date, gender, role ,manager_id,salary,address))
    
    mysql.connection.commit()
    cursor.close()

def update_employee(employee_id, data):
    from app import mysql  # Move import inside the function
    cursor = mysql.connection.cursor()
    if data['end_date'] == '':
        data['end_date'] = None
        
    cursor.execute('''
        UPDATE employees
        SET first_name=%s, last_name=%s, email=%s, phone=%s, department=%s, position=%s, hire_date=%s, salary=%s,end_date=%s,address=%s,manager_id=%s
        WHERE id=%s
    ''', (data['first_name'], data['last_name'], data['email'], data['phone'],
          data['department'], data['position'], data['hire_date'], data['salary'],  data['end_date'] ,data['address'],data['manager_id'],employee_id))
    
    mysql.connection.commit()
    cursor.close()

def delete_employee(employee_id):
    from app import mysql  # Move import inside the function
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM employees WHERE id=%s', (employee_id,))
    mysql.connection.commit()
    
    cursor.close()


def get_all_employee_data():
    from app import mysql  # Importing mysql inside the function to avoid circular imports
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, phone, department, position, hire_date, salary FROM employees')
    
    employees = cursor.fetchall()  # Fetch all rows from the result
    cursor.close()
    
    employee_list = []
    
    for employee in employees:
        employee_dict = {
            'id': employee[0],
            'first_name': employee[1],
            'last_name': employee[2],
            'email': employee[3],
            'phone': employee[4],
            'department': employee[5],
            'position': employee[6],
            'hire_date': employee[7],
            'salary': employee[8]
        }
        employee_list.append(employee_dict)
    
    return employee_list


def get_searched_employee_data(employee_id=None, employee_email=None):
    from app import mysql  # Importing mysql inside the function to avoid circular imports
    
    employee = None
    
    if employee_id:
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT id, first_name, last_name, email, phone, department, position, hire_date, salary FROM employees WHERE id = %s', (employee_id,))
        employee = cursor.fetchone()  # Fetch one row from the result
        cursor.close()
    
    elif employee_email:
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT id, first_name, last_name, email, phone, department, position, hire_date, salary FROM employees WHERE email = %s', (employee_email,))
        employee = cursor.fetchone()  # Fetch one row from the result
        cursor.close()

    if employee:
        employee_dict = {
            'id': employee[0],
            'first_name': employee[1],
            'last_name': employee[2],
            'email': employee[3],
            'phone': employee[4],
            'department': employee[5],
            'position': employee[6],
            'hire_date': str(employee[7]),  # Convert date to string if necessary
            'salary': str(employee[8])  # Convert salary to string if necessary
        }
        
        return employee_dict

    return None

# logged in user information fetching   
def get_employee_info_by_id(emp_id):
    
    from app import mysql  # Move import inside the function
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,first_name, last_name, salary, department, position, gender, role, hire_date, end_date,email, phone,manager_id,address FROM employees WHERE id=%s', (emp_id,))
    employee = cursor.fetchone()
    cursor.close()
    if employee:
        return employee  # Return tuple (id,email,role,password,)
   
    return None

# get all user information


def get_all_manager_data():
    from app import mysql  # Importing mysql inside the function to avoid circular imports

    # Open a cursor to perform the database query
    cursor = mysql.connection.cursor()

    # Execute the SQL query to fetch all managers (assuming managers are employees with the 'HR' role)
    cursor.execute("SELECT id, first_name, last_name FROM employees WHERE role = 'HR';")
    
    # Fetch all rows from the result
    managers_s = cursor.fetchall()
    
    # Close the cursor
    cursor.close()

    # Create a dictionary to store manager data
    managers_list = []
    managers = {}

    # Loop through the fetched results and map them by ID
    for manager in managers_s:
        manager_id = manager[0]
        full_name = f"{manager[1]} {manager[2]}"
        managers_list.append({"id":manager_id,"full_name":full_name})

    print(managers_list)
    # Return the dictionary containing managers' data
    return managers_list
    
    

def get_all_leave_types():
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT leave_type_id,leave_type FROM leave_types')
    leave_id_types = cursor.fetchall()
    cursor.close()
    
    leaves_types_list = []
    leaves_type_dict = {}
    
    for leave_id_type in leave_id_types:
        leaves_types_list.append({"leave_id":leave_id_type[0],"leave_type":leave_id_type[1]})
    
    
    return leaves_types_list



def apply_for_leave(leave_data,emp_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    
    # Assuming leave_data contains the fields: start_date, end_date, leave_type, reason
    start_date = leave_data.get('start_date')
    end_date = leave_data.get('end_date')
    leave_type = leave_data.get('leave_type')
    reason = leave_data.get('reason')
    
    try:
        # SQL query to insert leave data
        cursor.execute('''
            INSERT INTO leaves (id, start_date, end_date, leave_type_id, reason)
            VALUES (%s, %s, %s, %s, %s)
        ''', (emp_id, start_date, end_date, leave_type, reason))
        
        # Commit the changes to the database
        mysql.connection.commit()
    
    except Exception as e:
        mysql.connection.rollback()  # Rollback in case of error
        raise e  # Re-raise the exception for handling in the route
    
    finally:
        cursor.close()  # Ensure the cursor is closed after the operation

def get_leave_request_by_manager_id(manager_id):
    
    from app import mysql
    cursor = mysql.connection.cursor()
    
    get_leaves_by_manager_query = '''
                   SELECT l.leave_id, 
                        e.id AS employee_id, 
                        e.first_name, 
                        e.last_name,
                        lt.leave_type,
                        l.leave_status, 
                        l.reason, 
                        l.start_date, 
                        l.end_date 
                    FROM leaves l 
                    JOIN employees e ON l.id = e.id
                    JOIN leave_types lt ON l.leave_type_id = lt.leave_type_id
                    WHERE e.manager_id = %s;
                                    
                   '''
    cursor.execute(get_leaves_by_manager_query,(manager_id,))
    
    requests = cursor.fetchall()
    
    
    # Define the keys for the dictionary
    keys = ['leave_id', 'employee_id', 'first_name', 'last_name', 'leave_type','status', 'reason', 'start_date', 'end_date']
    
    # Create the list of dictionaries using a for loop
    list_of_requests = []
    for request in requests:
        request_dict = dict(zip(keys, request))  # Create a dictionary for each request
        list_of_requests.append(request_dict)  # Append it to the list
    
    cursor.close()  
    return list_of_requests


    
def update_status(new_status,leave_id,approved_by):
    
    from app import mysql
    
    cursor = mysql.connection.cursor()

    cursor.execute('''
        UPDATE leaves
        SET leave_status = %s,
            approved_by = %s
        WHERE leave_id = %s
    ''', (new_status, approved_by,leave_id))
        
    mysql.connection.commit()    
    cursor.close() 
    
    

    
def get_employee_all_info_by_id():
    from app import mysql
    cursor = mysql.connection.cursor()
    
    cursor.execute('SELECT * FROM')
    cursor.fetchone()
     
def get_avg_salary_hr_dashboard():
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT AVG(salary) FROM employees')
    avg_salary = cursor.fetchone()[0]  # Fetch the average salary
    cursor.close()

    return avg_salary

