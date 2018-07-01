from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_user import UserManager
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
babel = Babel()
mail = Mail()

login = LoginManager()
login.login_view = 'login'


def create_app(config_class=Config):
    """Create a Flask application.
    """
    # Set the version of the overall framework?
    __version__ = '0.1'

    # Instantiate Flask
    app = Flask(__name__)

    # Load environment variables
    app.config.from_object(config_class)

    # Enable CSRF protection globally
    csrf.init_app(app)

    # Initialize Flask-BabelEx
    babel.init_app(app)

    # Initialize Flask-Mail
    mail.init_app(app)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-Login
    login.init_app(app)

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    # Register blueprints
    from app.routes.main import main
    app.register_blueprint(main)

    from app.routes.teachers import teachers
    app.register_blueprint(teachers)

    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.api.admin import api_v1 as admin_api
    app.register_blueprint(admin_api, url_prefix='/api/v1')

    from app.routes.api.classes import api_v1 as classes_api
    app.register_blueprint(classes_api, url_prefix='/api/v1')

    from app.routes.api.teachers import api_v1 as teachers_api
    app.register_blueprint(teachers_api, url_prefix='/api/v1')

    from app.routes.api.docs import api as docs_api
    app.register_blueprint(docs_api, url_prefix='/api')

    return app


from app.models.auth import User

