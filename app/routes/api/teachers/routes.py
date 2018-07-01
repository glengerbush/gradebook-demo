from app import db
from app.models.main import Class, Teacher, teachers_classes
from app.routes.api.teachers import api_v1
from flask_user import roles_required, current_user
from flask import url_for, jsonify


@api_v1.route('/v1/teachers', methods=['GET'])
@roles_required(['admin'])
def teachers():
    # list of teachers
    if current_user.is_authenticated:
        if current_user.has_roles('admin'):
            teacher_list = list()
            for t in db.session.query(Teacher).all():
                teacher_list.append(t.serialize())
            return jsonify(teacher_list)
    return url_for('auth.login')


@api_v1.route('/v1/teachers/<int:teacher_id>', methods=['GET'])
@roles_required(['admin', 'teacher'])
def teacher(teacher_id):
    # returns teacher info
    if current_user.is_authenticated:
        if db.session.query(Teacher).with_entities(Teacher.userID).filter(Teacher.id == teacher_id).\
                one_or_none() == current_user or\
                current_user.has_roles('admin'):
            return jsonify(db.session.query(Teacher).filter(Teacher.id == teacher_id).one_or_none().serialize())
    return url_for('auth.login')


@api_v1.route('/v1/teachers/<int:teacher_id>/classes', methods=['GET'])
@roles_required(['admin', 'teacher'])
def teacher_classes(teacher_id):
    # returns a teachers classes
    if current_user.is_authenticated:
        if db.session.query(teachers_classes).with_entities(teachers_classes.c.TeacherID).\
                filter(teachers_classes.c.ClassID == teacher_id).one_or_none() == db.session.query(Teacher).\
                with_entities(Teacher.id).filter(Teacher.userID == current_user.id).one_or_none() or\
                current_user.has_roles('admin'):
            class_list = list()
            for classes in db.session.query(teachers_classes).with_entities(teachers_classes.c.ClassID).\
                    filter(teachers_classes.c.TeacherID == teacher_id).all():
                class_list.append(db.session.query(Class).with_entities(Class.id, Class.name).filter(Class.id == classes).one_or_none())
            return jsonify(class_list)
    return url_for('auth.login')
