from app import db
from app.models.main import BaseMixin
from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import login
from sqlalchemy.ext.hybrid import hybrid_property


####################################
#              Functions           #
####################################

@login.user_loader
def load_user(id_):
    return User.query.get(int(id_))


####################################
#            Fixed Lists           #
####################################


####################################
#               Tables             #
####################################


class User(BaseMixin, UserMixin, db.Model):

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    # User fields
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # misc
    registered = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<{}, {} {}>'.format(self.username, self.first, self.last)

    @hybrid_property
    def first(self):
        return '{0}'.format(self.first_name)

    @hybrid_property
    def last(self):
        return '{0}'.format(self.last_name)

    @hybrid_property
    def name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


# defined as required by Flask 1.0
class Role(db.Model):
    ####################################
    #            WARNING               #
    # name recommended by flask!!!!#
    ####################################
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# defined as required by Flask 1.0
class UserRoles(db.Model):
    ####################################
    #            WARNING               #
    # name recommended by flask!!!!#
    ####################################
    __tablename__ = 'user_roles'
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
