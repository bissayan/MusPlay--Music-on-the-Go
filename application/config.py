import os, secrets
from datetime import timedelta


# Import the os module to interact with the operating system
import os

# Define the base directory as the absolute path of the directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Define a base configuration class
class Config():
    # Turn off debug mode by default
    DEBUG = False
    # Set the SQLite database directory to None by default
    SQLITE_DB_DIR = None
    # Set the SQLAlchemy database URI to None by default
    SQLALCHEMY_DATABASE_URI = None
    # Turn off SQLAlchemy's event system, which can consume a lot of resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Define a configuration class for local development
class LocalDev(Config):
    # # Set the SQLite database directory to the db directory in the base directory
    # SQLITE_DB_DIR = os.path.join(basedir, './db')
    # # Set the SQLAlchemy database URI to the SQLite database in the db directory
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, '22f3001500-MAD-1.sqlite3')  # Required for the application to work

    # Set the secret key for Flask-Security
    #SECRET_KEY = 'your-secret-key'  
    # Set the password hash method for Flask-Security
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Required for the application to work
    # Set the password salt for Flask-Security
    SECURITY_PASSWORD_SALT = secrets.SystemRandom().getrandbits(128)  # Required for the application to work
    # Enable user registration in Flask-Security
    SECURITY_REGISTERABLE = True
    # Enable role joining in Flask-Security
    SECURITY_JOIN_USER_ROLES = True
    # Enable user tracking in Flask-Security
    SECURITY_TRACKABLE = True

    # CSRF_ENABLED = True

    # Set the post-login view for Flask-Security
    SECURITY_POST_LOGIN_VIEW = '/logged_in'
    # Set the post-logout view for Flask-Security
    SECURITY_POST_LOGOUT_VIEW = '/bye'

    # Disable automatic sending of registration confirmation email for simplicity
    SECURITY_SEND_REGISTER_EMAIL = False
    # Set the subject of the registration email
    SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to My App'

    # Configure an email extension for Flask-Security
    SECURITY_EMAIL_SENDER = 'your_email@example.com'  # Replace with your email address
    SECURITY_EMAIL_REGISTERABLE = True
    # SECURITY_LOGIN_URL = '/auth/login'
    # SECURITY_LOGIN_USER_TEMPLATE = 'login_test.html'
    # Turn on debug mode for local development
    #UPLOAD_FOLDER = os.path.join(app.root_path,  'say2vue', 'public', 'static', 'song_store')
    SQLALCHEMY_DATABASE_URI= 'sqlite:///22f3001500-MAD-1.sqlite3'
#app.config['SECRET KEY']='thisasecretkey'
    #SECRET_KEY = 'your_secret_key_here'
    #JSON_AS_ASCII = False
    DEBUG = True

# Define a configuration class for production
class ProductionDev(Config):
    # Set the SQLite database directory to the db_directory in the parent of the base directory
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')
    # Set the SQLAlchemy database URI to the SQLite database in the db_directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, '22f3001500-MAD-1.sqlite3')  # Required for the application to work
    # Turn off debug mode for production
    DEBUG = False