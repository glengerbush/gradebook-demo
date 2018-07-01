from app import db
from app.models.main import BaseMixin, students_classes
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import UniqueConstraint
from collections import OrderedDict


####################################
#            Fixed Lists           #
####################################
# none

####################################
#               Tables             #
####################################


class Score(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', onupdate="CASCADE", ondelete="CASCADE"),
                           primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id', onupdate="CASCADE", ondelete="CASCADE"),
                              primary_key=True)
    score = db.Column(db.Integer, index=True)
    __table_args__ = (UniqueConstraint('student_id', 'assignment_id', name='score_id'),)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def serialize(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)

        return result


class Assignment(BaseMixin, db.Model):
    name = db.Column(db.VARCHAR(128), index=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))
    assignment_category_id = db.Column(db.Integer, db.ForeignKey('assignmentcategory.id', ondelete='SET NULL'))
    total_points = db.Column(db.Integer)
    date = db.Column("Date", db.DATE, index=True)
    score = db.relationship(Score, backref='Assignment', cascade="all, delete-orphan", passive_deletes=True)


def add_null_scores(mapper, connection, target):
    student_ids_list = db.session.query(students_classes).with_entities(students_classes.c.student_id).filter(
        students_classes.c.class_id == target.class_id).all()
    for id_ in student_ids_list:
        new_score = Score()
        new_score.assignment_id = target.id
        new_score.student_id = id_
        db.session.add(new_score)


event.listen(Assignment, 'after_insert', add_null_scores)


class AssignmentCategory(BaseMixin, db.Model):
    category = db.Column(db.VARCHAR(64), index=True)
    weight = db.Column(db.Integer, index=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    assignment = db.relationship("Assignment", backref="AssignmentCategory")
