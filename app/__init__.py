from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from app.models import get_user_by_id

mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # MySQL configurations
    app.config.from_object('app.config.Config')
    app.secret_key = 'your_secret_key'

    mysql.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Redirect users to login page

    from app.routes import main
    app.register_blueprint(main)

    return app


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)