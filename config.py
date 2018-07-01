import os


class Config(object):
    # General Settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or True
    CSRF_ENABLED = True

    #SERVER_NAME = os.environ.get('SERVER_NAME') or 'localhost'

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = '"Gradebook Demo" <noreply@gradebookdemo.com>'

    # Flask-User settings
    USER_APP_NAME = "Gradebook Demo"      # Shown in email templates and page footers
    USER_ENABLE_USERNAME = True
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_REGISTER = False
    USER_ENABLE_REMEMBER_ME = True
    USER_ENABLE_EMAIL = True
    USER_ENABLE_MULTIPLE_EMAILS = False
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@gradebookdemo.com"
    USER_RESET_PASSWORD_EXPIRATION = 600
    USER_CONFIRM_EMAIL_EXPIRATION = 87400

    # Flask endpoint settings
    USER_AFTER_CHANGE_PASSWORD_ENDPOINT = ''
    USER_AFTER_CHANGE_USERNAME_ENDPOINT = ''
    USER_AFTER_CONFIRM_ENDPOINT = ''
    USER_AFTER_EDIT_USER_PROFILE_ENDPOINT = ''
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = ''
    USER_AFTER_LOGIN_ENDPOINT = 'main.user_home'
    USER_AFTER_LOGOUT_ENDPOINT = ''
    USER_AFTER_REGISTER_ENDPOINT = ''
    USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = ''
    USER_AFTER_RESET_PASSWORD_ENDPOINT = ''
    USER_AFTER_INVITE_ENDPOINT = ''
    USER_UNAUTHENTICATED_ENDPOINT = 'user.login'
    USER_UNAUTHORIZED_ENDPOINT = ''

