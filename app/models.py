from datetime import datetime
from flask_login import UserMixin
from flask import jsonify


class User(UserMixin):
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

def get_user_by_id(user_id):
    from app import mysql  
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,email,role FROM employees WHERE id=%s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(id=user[0], email=user[1], role=user[2])
    return None

def get_user_by_email(email):
    from app import mysql  
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,email,role,password FROM employees WHERE email=%s', (email,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return user  
    return None

def add_employee(data):
    from app import mysql  
   
   
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
    from app import mysql  
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
    from app import mysql  
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM employees WHERE id=%s', (employee_id,))
    mysql.connection.commit()
    
    cursor.close()


def get_all_employee_data():
    from app import mysql 
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, phone, department, position, hire_date, salary FROM employees')
    
    employees = cursor.fetchall()  
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
    from app import mysql 
    
    employee = None
    
    if employee_id:
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT id, first_name, last_name, email, phone, department, position, hire_date, salary FROM employees WHERE id = %s', (employee_id,))
        employee = cursor.fetchone()  
        cursor.close()
    
    elif employee_email:
        cursor = mysql.connection.cursor()
        cursor.execute(f'SELECT id, first_name, last_name, email, phone, department, position, hire_date, salary FROM employees WHERE email = %s', (employee_email,))
        employee = cursor.fetchone()  
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
            'hire_date': str(employee[7]),
            'salary': str(employee[8])  
        }
        
        return employee_dict

    return None

def get_employee_info_by_id(emp_id):
    
    from app import mysql 
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,first_name, last_name, salary, department, position, gender, role, hire_date, end_date,email, phone,manager_id,address FROM employees WHERE id=%s', (emp_id,))
    employee = cursor.fetchone()
    cursor.close()
    if employee:
        return employee  
   
    return None



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
    
    

    
def get_employee_all_info_by_id(emp_id):
    from app import mysql
    cursor = mysql.connection.cursor()
    
    cursor.execute(f'SELECT * FROM employees where id ={emp_id}')
    employee_data = cursor.fetchone()
    
    return employee_data
    
def get_leaves_taken_this_year():
    
    return 

     
def get_avg_salary_hr_dashboard():
    from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT AVG(salary) FROM employees')
    avg_salary = cursor.fetchone()[0]  # Fetch the average salary
    cursor.close()

    return avg_salary

    
# models.py
from flask import current_app

import pandas as pd

def fetch_data(query):
    
    from app import mysql
    
    with current_app.app_context():
        cursor = mysql.connection.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(data, columns=columns)
        finally:
            cursor.close()  

    return df



def get_dashboard_data(department):
    from app import mysql

    
    data = dict()

 
    with mysql.connection.cursor() as cursor:
        
        if department == 'All':
            cursor.execute('SELECT AVG(salary) FROM employees;')
        else:
            cursor.execute('SELECT AVG(salary) FROM employees WHERE department = %s;', (department,))
        
        avg_salary = cursor.fetchone()[0]  
        
        
        if avg_salary is None:
            avg_salary = 0  
       
        if department == 'All':
            cursor.execute('SELECT COUNT(*) FROM employees;')
        else:
            cursor.execute('SELECT COUNT(*) FROM employees WHERE department = %s;', (department,))
        
        total_employees = cursor.fetchone()[0]
        
        if department == 'All':
            cursor.execute('SELECT SUM(salary) as total_salary FROM employees;')
        else:
            cursor.execute('SELECT SUM(salary) as salary FROM employees WHERE department = %s;', (department,))
            
        total_salary =   cursor.fetchone()[0]
            
      
        

    # Populate the data dictionary
    data['average_salary'] = avg_salary
    data['total_employees'] = total_employees
    data['total_salary_employees'] = total_salary
    return data




import pandas as pd

def get_dashboard_data_2(department):
    
    from app import mysql

    # Use a context manager for cursor
    with mysql.connection.cursor() as cursor:
        # Query to get average salary for each department
        cursor.execute('SELECT department, AVG(salary) AS average_salary FROM employees GROUP BY department;')
        
        # Fetch all results
        results = cursor.fetchall()

    # Create a DataFrame from the results
    df = pd.DataFrame(results, columns=['Department', 'Average Salary'])

    # Optionally: Add total employees per department
    total_employees_query = 'SELECT department, COUNT(*) AS total_employees FROM employees GROUP BY department;'
    
    with mysql.connection.cursor() as cursor:
        cursor.execute(total_employees_query)
        total_results = cursor.fetchall()
    
    # Create a DataFrame for total employees
    total_df = pd.DataFrame(total_results, columns=['Department', 'Total Employees'])

    # Merge the two DataFrames on 'Department'
    merged_df = pd.merge(df, total_df, on='Department', how='outer')

    return merged_df


def insert_payroll_data(employee_id, salary, deductions, bonuses, total_pay): 
    from app import mysql
    
    employee = None
    with mysql.connection.cursor() as cursor:
        
        cursor.execute(
            "INSERT INTO payroll (employee_id, salary, deductions, bonuses, total_pay, created_at) VALUES (%s, %s, %s, %s, %s, NOW())",
            (employee_id, salary, deductions, bonuses, total_pay)
        )
        
        mysql.connection.commit()

        
        cursor.execute("SELECT first_name,last_name, position FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        print(employee)
    
    return employee


# Fetch payroll history for a specific employee
def fetch_payroll_history(employee_id):
    from app import mysql

    query = """
    SELECT 
        MONTH(created_at) AS month, 
        salary, 
        deductions, 
        bonuses, 
        (salary - deductions + bonuses) AS total_pay 
    FROM payroll 
    WHERE employee_id = %s 
    ORDER BY MONTH(created_at) DESC
    """

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute(query, (employee_id,))  # Use parameterized query to prevent SQL injection
            results = cursor.fetchall()
            
        # Map results to a list of dictionaries
        payroll_history = [
            {
                'month': row[0],
                'salary': row[1],
                'deductions': row[2],
                'bonuses': row[3],
                'total_pay': row[4]
            }
            for row in results
        ]

        return payroll_history

    except Exception as e:
        print(f"Error fetching payroll history: {e}")
        return []