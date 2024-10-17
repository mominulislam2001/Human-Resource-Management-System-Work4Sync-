from flask_login import  current_user


def is_hr():
    return current_user.is_authenticated and current_user.role == 'HR'

def is_employee():
    return current_user.is_authenticated and current_user.role == 'Employee'

def is_manager():
    return current_user.is_authenticated and current_user.role == 'Manager'