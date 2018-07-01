from app import db
from app.models.main import Student, Teacher, Class, teachers_classes, students_classes
from app.models.gradebook import Assignment, Score, AssignmentCategory
from app.routes.api.classes import api_v1
from flask_user import roles_required, current_user
from flask import url_for, jsonify, redirect, request, render_template, render_template_string
from sqlalchemy import and_, asc, desc
from sqlalchemy.sql import func
import datetime


def owns_class(class_id):
    teacher_id = db.session.query(Teacher).with_entities(Teacher.id).filter(
        Teacher.user_id == current_user.id).one_or_none()
    return db.session.query(teachers_classes).with_entities(teachers_classes.c.teacher_id). \
            filter(and_(teachers_classes.c.class_id == class_id, teachers_classes.c.teacher_id == teacher_id)).scalar():

    
@api_v1.route('/classes', methods=['GET'])
@roles_required(['admin'])
def all_classes():
    if current_user.is_authenticated:
        if current_user.has_roles('admin'):
            allclasses = list()
            for i in db.session.query(Class).all():
                allclasses.append(i.serialize())
            return jsonify(allclasses)
    return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>', methods=['GET'])
@roles_required(['admin', 'teacher'])
def class_by_id(class_id):
    if current_user.is_authenticated:
        if owns_class(class_id) or current_user.has_roles('admin'):
            return jsonify(db.session.query(Class).filter(Class.id == class_id).one_or_none().serialize())
    return redirect(url_for('auth.login'))


@api_v1.route('/class_details/<int:class_id>')
@roles_required(['admin', 'teacher'])
def class_details(class_id):
    if current_user.has_roles('admin') or owns_class(class_id):
        class_ = db.session.query(Class).filter(Class.id == class_id).one_or_none()
        assignment_categories = db.session.query(AssignmentCategory).filter(AssignmentCategory.class_id == class_id).all()
        assignments = db.session.query(Assignment).filter(Assignment.class_id == class_id).all()
        student_list = db.session.query(students_classes).with_entities(students_classes.c.student_id).filter(
            students_classes.c.class_id == class_id).all()
        assignment_list = db.session.query(Assignment).with_entities(Assignment.id).filter(
            Assignment.class_id == class_id).order_by(asc(Assignment.date)).all()
        scores = db.session.query(Score).filter(Score.assignment_id.in_(assignment_list)).all()
        enrollment = len(student_list)
        if class_.in_session:
            return render_template('teacher/class.html', class_=class_, assignment_categories=assignment_categories,
                               assignments=assignments, scores=scores,
                               assignment_categories_col=[("Category:", "category"), ("Weight:", "weight")],
                               enrollment=enrollment)
        else:
            return render_template('teacher/old_class.html', class_=class_, assignment_categories=assignment_categories,
                                   assignments=assignments, scores=scores,
                                   assignment_categories_col=[("Category:", "category"), ("Weight:", "weight")],
                                   enrollment=enrollment)


####################################
#           Scores(Grades)         #
####################################
assignment_label = "Assignment"
score_label = "score"


@api_v1.route('/classes/<int:class_id>/grades', methods=['GET'])
@roles_required(['admin', 'teacher'])
def get_grades_json(class_id):
    if owns_class(class_id) or current_user.has_roles('admin'):
        student_ids_list = db.session.query(students_classes).with_entities(students_classes.c.student_id).filter(
            students_classes.c.class_id == class_id).all()
        student_ids_list = [i[0] for i in student_ids_list]
        student_info = db.session.query(Student).with_entities(Student.id, Student.last, Student.first).filter(
            Student.id.in_(student_ids_list)).all()
        assignment_info = db.session.query(Assignment).filter(Assignment.class_id == class_id).order_by(
            asc(Assignment.date)).all()
        assignment_list = [i.id for i in assignment_info]
        all_scores = db.session.query(Score).filter(Score.assignment_id.in_(assignment_list)).all()
        scores = {}
        for id_ in student_ids_list:
            scores[id_] = {}
        for score in all_scores:
            scores[score.student_id][score.assignment_id] = score.score
        overall = overall_score(student_ids_list, assignment_list, class_id)
        return render_template('json/data_grades.json', objects=[student_info, assignment_info, scores],
                               object_types=["Student", "Assignment", "Score"],
                               column_lists=[['id', 'last', 'first'], ['id', 'name', 'date']], overall_score=overall,
                               pick_dict=assignment_cat_pick(class_id))
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/grades/<string:student_ids_string>', methods=['PUT'])
@roles_required(['admin', 'teacher'])
def update_grades_json(class_id, student_ids_string):
    if owns_class(class_id) or current_user.has_roles('admin'):
        id_list = student_ids_string.split(",")
        data = request.get_json()
        for id_ in id_list:
            scores = db.session.query(Score).filter(
                and_(Score.student_id == int(id_), Score.assignment_id.in_(data[id_][assignment_label].keys()))).all()
            for score_object in scores:
                score = data[str(score_object.student_id)][assignment_label][str(score_object.assignment_id)][
                    score_label]
                if score == '':
                    score = None
                else:
                    score = int(score)
                setattr(score_object, score_label, score)
        db.session.commit()

        # convert string list to integers for filtering
        id_list = list(map(int, id_list))
        student_info = db.session.query(Student).with_entities(Student.id, Student.last, Student.first).filter(
            Student.id.in_(id_list)).all()
        assignment_info = db.session.query(Assignment).with_entities(
            Assignment.id, Assignment.name, Assignment.date).filter(Assignment.class_id == class_id).order_by(
            asc(Assignment.date)).all()
        assignment_list = [i.id for i in assignment_info]
        all_scores = db.session.query(Score).filter(and_(Score.assignment_id.in_(assignment_list), Score.student_id.in_(id_list))).all()
        scores = {}
        for id_ in id_list:
            scores[id_] = {}
        for score in all_scores:
            scores[score.student_id][score.assignment_id] = score.score
        overall = overall_score(id_list, assignment_list, class_id)
        return render_template('json/data_grades.json', objects=[student_info, assignment_info, scores],
                               object_types=["Student", "Assignment", "Score"],
                               column_lists=[['id', 'last', 'first'], ['id', 'name', 'date']], overall_score=overall,
                               pick_dict=assignment_cat_pick(class_id))
    else:
        return redirect(url_for('auth.login'))


def overall_score(student_list, assignment_list, class_id):
    # makes a dictionary that where the AssignmentCategory.id is the key to the AssignmentCategory.weight
    weight_cat_dict = db.session.query(AssignmentCategory).with_entities(AssignmentCategory.id,
                                                                         AssignmentCategory.weight).filter(
        AssignmentCategory.class_id == class_id).all()
    weight_cat_dict = dict(weight_cat_dict)
    assignments_cat_dict = db.session.query(Assignment).with_entities(Assignment.id,
                                                                      Assignment.assignment_category_id).filter(
        Assignment.id.in_(assignment_list)).all()
    assignments_cat_dict = dict(assignments_cat_dict)
    assignments = db.session.query(Assignment).filter(Assignment.id.in_(assignment_list)).all()

    # make a dictionary of overall scores, where the student id's are the keys
    # initialize grades which will be dict of dict, takes [student id][assignment category]
    scores = dict()
    grades = {}
    assignment_cat_total_possible = {}
    total_weight = {}
    for id_ in student_list:
        scores[id_] = db.session.query(Score).filter(
            and_(Score.student_id == id_, Score.assignment_id.in_(assignment_list))).all()
        grades[id_] = {}
        assignment_cat_total_possible[id_] = {}
        total_weight[id_] = 0
        for key in weight_cat_dict:
            assignment_cat_total_possible[id_][key] = 0
        for assignment in assignments:
            if assignment.assignment_category_id and assignment.total_points:
                if db.session.query(Score.score).filter(Score.assignment_id == assignment.id).filter(Score.student_id == id_).first()[0] is not None:
                    assignment_cat_total_possible[id_][assignment.assignment_category_id] += assignment.total_points
        for key in weight_cat_dict:
            if assignment_cat_total_possible[id_][key]:
                total_weight[id_] += weight_cat_dict[key]

    for key in scores:
        for score in scores[key]:
            assignment_category = assignments_cat_dict[score.assignment_id]
            if not grades[score.student_id].get(assignment_category):
                grades[score.student_id][assignment_category] = 0
            if score.score:
                grades[score.student_id][assignment_category] += score.score
            else:
                grades[score.student_id][assignment_category] += 0

    overall = dict()

    for id_ in student_list:
        if total_weight[id_]:
            overall[id_] = 0.0
            for key in weight_cat_dict:
                if grades[id_].get(key) and assignment_cat_total_possible[id_][key]:
                    grade_in_this_cat = float(grades[id_][key])
                    weight = float(weight_cat_dict[key])
                    overall[id_] += (grade_in_this_cat / float(assignment_cat_total_possible[id_][key])) * weight
            overall[id_] = round(overall[id_] / total_weight[id_], 2)
        else:
            overall[id_] = 0.0
    return overall


####################################
#            Assignments           #
####################################

def assignment_cat_pick(class_id):
    return dict(db.session.query(AssignmentCategory).with_entities(
        AssignmentCategory.id, AssignmentCategory.category).filter(AssignmentCategory.class_id == class_id).all())


pick_what = ["AssignmentCategory", "category", "assignment_category_id"]

assignment_obj_type = "Assignment"


@api_v1.route('/classes/<int:class_id>/assignments', methods=['GET'])
@roles_required(['admin', 'teacher'])
def get_assignments_json(class_id):
    if owns_class(class_id) or current_user.has_roles('admin'):
        object_list = db.session.query(Assignment).filter(Assignment.class_id == class_id).all()
        return render_template('json/data_dropdown.json', objects=object_list, object_type=assignment_obj_type,
                               column_list=Assignment.__mapper__.c.keys(),
                               pick_dict=assignment_cat_pick(class_id),
                               pick_what=pick_what, send_pick_list=True)
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/assignments', methods=['POST'])
@roles_required(['admin', 'teacher'])
def create_assignments_json(class_id):
    if owns_class(class_id) or current_user.has_roles('admin'):
        data = request.get_json()
        new_row = Assignment()
        for key, value in data["0"][assignment_obj_type].items():
            if value == '':
                value = None
            setattr(new_row, key, value)
        setattr(new_row, "class_id", class_id)
        db.session.add(new_row)
        db.session.commit()
        object_list = list()
        object_list.append(new_row)
        return render_template('json/data_dropdown.json', objects=object_list, object_type=assignment_obj_type,
                               column_list=Assignment.__mapper__.c.keys(),
                               pick_dict=assignment_cat_pick(class_id),
                               pick_what=pick_what)
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/assignments/<string:ids_string>', methods=['PUT'])
@roles_required(['admin', 'teacher'])
def update_assignment_json(class_id, ids_string):
    if owns_class(class_id) or current_user.has_roles('admin'):
        # for really large bulk edits, a more efficient solution should be used
        # create list of strings containing all ids being updated
        id_list = ids_string.split(",")
        data = request.get_json()
        for id_ in id_list:
            assignment = db.session.query(Assignment).filter(Assignment.id == id_).one_or_none()
            for key, value in data[id_][assignment_obj_type].items():
                setattr(assignment, key, value)
        db.session.commit()
        # convert string list to integers for filtering
        id_list = list(map(int, id_list))
        object_list = db.session.query(Assignment).filter(Assignment.id.in_(id_list)).all()
        return render_template('json/data_dropdown.json', objects=object_list, object_type=assignment_obj_type,
                               column_list=Assignment.__mapper__.c.keys(),
                               pick_dict=assignment_cat_pick(class_id),
                               pick_what=pick_what)
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/assignments/<string:ids_string>', methods=['DELETE'])
@roles_required(['admin', 'teacher'])
def delete_assignments_json(class_id, ids_string):
    if owns_class(class_id) or current_user.has_roles('admin'):
        # create list of strings containing all ids being deleted and then convert to integers for filtering
        id_list = ids_string.split(",")
        id_list = list(map(int, id_list))
        db.session.query(Assignment).filter(Assignment.id.in_(id_list)).delete(synchronize_session=False)
        db.session.commit()
        return render_template_string("{}")
    else:
        return redirect(url_for('auth.login'))


####################################
# Categories(AssignmentCategories) #
####################################

@api_v1.route('/classes/<int:class_id>/assignment_categories', methods=['GET'])
@roles_required(['admin', 'teacher'])
def get_assignment_categories_json(class_id):
    if owns_class(class_id) or current_user.has_roles('admin'):
        object_list = db.session.query(AssignmentCategory).filter(AssignmentCategory.class_id == class_id).all()
        extra = cat_class_avg(object_list)
        return render_template('json/data.json', objects=object_list,
                               column_list=AssignmentCategory.__mapper__.c.keys(), extra_name="class_avg", extra=extra)
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/assignment_categories', methods=['POST'])
@roles_required(['admin', 'teacher'])
def create_assignment_categories_json(class_id):
    if owns_class(class_id) or current_user.has_roles('admin'):
        data = request.get_json()
        new_row = AssignmentCategory()
        for key, value in data["0"].items():
            if value == '':
                value = None
            if key == "weight":
                if "%" in value:
                    value = value.strip('%')
                if safe_add_to_total_weight(value, class_id):
                    setattr(new_row, key, value)
                else:
                    db.session.rollback()
                    return render_template('json/error_message/too_much_weight.json')
            else:
                setattr(new_row, key, value)
        setattr(new_row, "class_id", class_id)
        db.session.add(new_row)
        db.session.commit()
        object_list = list()
        object_list.append(new_row)
        extra = dict()
        extra[new_row.id] =  "0%"
        return render_template('json/data.json', objects=object_list,
                               column_list=AssignmentCategory.__mapper__.c.keys(), extra_name="class_avg", extra=extra)
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/assignment_categories/<string:ids_string>', methods=['PUT'])
@roles_required(['admin', 'teacher'])
def update_assignment_categories_json(class_id, ids_string):
    if owns_class(class_id) or current_user.has_roles('admin'):
        # for really large bulk edits, a more efficient solution should be used
        # create list of strings containing all ids being updated
        id_list = ids_string.split(",")
        data = request.get_json()
        for id_ in id_list:
            assignment_category = db.session.query(AssignmentCategory).filter(
                AssignmentCategory.id == id_).one_or_none()
            for key, value in data[id_].items():
                if key == "weight":
                    if "%" in value:
                        value = value.strip('%')
                    if safe_add_to_total_weight(value, class_id):
                        setattr(assignment_category, key, value)
                    else:
                        db.session.rollback()
                        return render_template('json/too_much_weight.json')
                else:
                    setattr(assignment_category, key, value)
        db.session.commit()
        # convert string list to integers for filtering
        id_list = list(map(int, id_list))
        object_list = db.session.query(AssignmentCategory).filter(AssignmentCategory.id.in_(id_list)).all()
        extra = cat_class_avg(object_list)
        return render_template('json/data.json', objects=object_list,
                               column_list=AssignmentCategory.__mapper__.c.keys(), extra_name="class_avg", extra=extra)
    else:
        return redirect(url_for('auth.login'))


@api_v1.route('/classes/<int:class_id>/assignment_categories/<string:ids_string>', methods=['DELETE'])
@roles_required(['admin', 'teacher'])
def delete_assignment_categories_json(class_id, ids_string):
    if owns_class(class_id) or current_user.has_roles('admin'):
        # create list of strings containing all ids being deleted and then convert to integers for filtering
        id_list = ids_string.split(",")
        id_list = list(map(int, id_list))
        db.session.query(AssignmentCategory).filter(AssignmentCategory.id.in_(id_list)).delete(
            synchronize_session=False)
        db.session.commit()
        return render_template_string("{}")
    else:
        return redirect(url_for('auth.login'))


def safe_add_to_total_weight(new_weight, class_id):
    current_total = db.session.query(func.sum(AssignmentCategory.weight).label("current_total")).filter(
        AssignmentCategory.class_id == class_id).all()
    if current_total[0][0]:
        if int(current_total[0][0]) + int(new_weight) > 100:
            return False
        else:
            return True
    else:
        return True


def cat_class_avg(all_cats):
    extra = {}
    total_cat_points = {}
    total_cat_score = {}
    for cat in all_cats:
        all_assignments = db.session.query(Assignment).filter(Assignment.assignment_category_id == cat.id).all()
        total_cat_points[cat.id] = 0
        total_cat_score[cat.id] = 0
        extra[cat.id] = "0%"
        for assignment in all_assignments:
            total_cat_points[cat.id] += assignment.total_points
            temp_scores = db.session.query(func.sum(Score.score).label("total_scored"),
                                           func.count(Score.score).label("scores_count")).filter(
                Score.assignment_id == assignment.id).all()
            if temp_scores[0][0] and temp_scores[0][1]:
                total_cat_score[cat.id] += temp_scores[0][0] / temp_scores[0][1]

    for key in total_cat_points:
        if total_cat_points[key]:
            temp_avg = (float(total_cat_score[key]) / float(total_cat_points[key])) * 100
            extra[key] = str(int(round(temp_avg, 0))) + "%"
    return extra
