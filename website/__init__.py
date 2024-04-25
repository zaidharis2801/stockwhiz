from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import create_engine
from os import path
from flask_mail import Mail
from flask_login import LoginManager
import os



# Database selector: 'oracle' or 'sqlite'
DATABASE = 'sqlite'  # Change to 'oracle' to use Oracle

db = SQLAlchemy()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')

# Initialize database URI and engine
SQLALCHEMY_DATABASE_URI = None
engine = None

# Oracle setup
if DATABASE == 'oracle':
    DIALECT = 'oracle'
    SQL_DRIVER = 'cx_oracle'
    USERNAME = 'c##se'  # enter your username
    PASSWORD = 'a1234'  # enter your password
    HOST = 'localhost'  # enter the oracle db host url
    PORT = 1521  # enter the oracle port number
    SERVICE = 'orcl'  # enter the oracle db service name
    SQLALCHEMY_DATABASE_URI = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD + '@' + HOST + ':' + str(
        PORT) + '/?service_name=' + SERVICE
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

# SQLite setup
elif DATABASE == 'sqlite':
    DB_NAME = "database.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

loginn_manager = LoginManager()

# #test query
# import pandas as pd
# test_df = pd.read_sql_query('SELECT * FROM SALES', engine)
# print(test_df)

def create_app():
    # app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'fsfhsdfhsufsfsifd'
    # app.config['SQLALCHEMY_DATABASE_URI'] = ENGINE_PATH_WIN_AUTH
    #
    # APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    # UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #
    # db.init_app(app)

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fsfhsdfhsufsfsifd'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)



    # login = LoginManager(app)
    # login.login_view = 'views.home'

    from .views import views
    from .auth import auth
    from .chart import chart
    from .emailclass import email
    from .payment import payment
    from .account import account
    from .transactions import transactions
    from .stocks import stocks

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(chart, url_prefix='/')
    app.register_blueprint(email, url_prefix='/')
    app.register_blueprint(payment, url_prefix='/')
    app.register_blueprint(account, url_prefix='/')
    app.register_blueprint(transactions, url_prefix='/')
    app.register_blueprint(stocks, url_prefix='/')

    from .models import User, Transactions, Search


    create_database(app)
    loginn_manager.login_view = 'auth.login'
    loginn_manager.init_app(app)

    @loginn_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    Mail(app)


    return app


def send_mail(x):
    x.config['MAIL_SERVER'] = 'smtp.gmail.com'
    x.config['MAIL_PORT'] = 465
    x.config['MAIL_USERNAME'] = 'adhdestinies@gmail.com'
    x.config['MAIL_PASSWORD'] = 'ufcjvdlrhjdbhwco'
    x.config['MAIL_USE_TLS'] = False
    x.config['MAIL_USE_SSL'] = True
    x.config['MAIL_DEFAULT_SENDER'] = ('Muhammad Hur', 'adhdestinies@gmail.com')
    Mail(x)




def create_database(app):
    if not path.exists('website/database.db'):
        db.create_all(app=app)
        # print('Created Database!')
