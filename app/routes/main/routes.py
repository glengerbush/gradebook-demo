from app.routes.main import main
from flask_login import login_required
from flask import render_template, render_template_string
from flask import redirect, url_for
from flask_user import current_user
from app import db
from app.models.main import Class, teachers_classes, Teacher
from sqlalchemy import and_

###############################
#        Landing Page         #
###############################

@main.route('/')
@main.route('/index')
def index():
    return redirect(url_for('user.login'))


###############################
#           Redirects         #
###############################


###############################
#          Main pages         #
###############################

@main.route('/home')
@login_required
def user_home():
    # direct to correct profile page or admin overview
    if current_user.has_roles('admin'):
        render_template_string("<h1>Admin view under construction</h1>")
    elif current_user.has_roles('teacher'):
        teacher_id = db.session.query(Teacher).with_entities(Teacher.id).filter(
            Teacher.user_id == current_user.id).one_or_none()
        class_ids = db.session.query(teachers_classes).with_entities(teachers_classes.c.class_id).filter(
            teachers_classes.c.teacher_id == teacher_id).all()
        class_list = db.session.query(Class).filter(and_(Class.id.in_(class_ids), Class.in_session == True)).all()
        old_classes = db.session.query(Class).filter(and_(Class.id.in_(class_ids), Class.in_session == False)).all()
        return render_template('teacher/overview.html', class_list=class_list, old_classes=old_classes)
    else:
        return render_template_string("<h1>Site Administrator has not assigned you a role, please contact info@gradebookdemo.com</h1>")


@main.route('/profile')
@login_required
def profile():
    # List all user info
    if current_user.has_roles('teacher'):
        teacher = db.session.query(Teacher).filter(Teacher.user_id == current_user.id).one_or_none()
        return render_template('teacher/profile.html', teacher=teacher)
    else:
        return render_template_string("<h1>Profile not available, please contact info@gradebookdemo.com</h1>")
