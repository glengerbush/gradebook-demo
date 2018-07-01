from app import db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref
from sqlalchemy.ext.hybrid import hybrid_property
from collections import OrderedDict


# CHAR/VARCHAR Lengths
StudentIDLength = 8
PhoneLength = 12
StandardLength = 128

####################################
#                  Base           #
####################################


class BaseMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)

        return result


####################################
#                Mixins            #
####################################

class AddressMixin(object):
    street_address = db.Column("Street Address", db.VARCHAR(StandardLength), index=True)
    apt = db.Column(db.VARCHAR(32), index=True)
    city = db.Column(db.VARCHAR(StandardLength), index=True)
    state = db.Column(db.CHAR(2), index=True)
    zip_code = db.Column("Zip Code", db.Integer, index=True)
    neighborhood = db.Column(db.VARCHAR(StandardLength), index=True)


class ContactMixin(AddressMixin):
    phone = db.Column('Phone', db.VARCHAR(PhoneLength), index=True)
    secondary_phone = db.Column("Secondary Phone", db.VARCHAR(PhoneLength), index=True)
    email = db.Column(db.VARCHAR(StandardLength), index=True)
    secondary_email = db.Column("Secondary Email", db.VARCHAR(StandardLength), index=True)


class NameMixin(object):
    first = db.Column(db.VARCHAR(StandardLength), index=True)
    last = db.Column(db.VARCHAR(StandardLength), index=True)
    dob = db.Column(db.Date, index=True)

    @hybrid_property
    def full_name(self):
        return '{0}, {1}'.format(self.last, self.first)


####################################
#            Fixed Lists           #
####################################


class Subject(BaseMixin, db.Model):
    name = db.Column(db.VARCHAR(StandardLength), unique=True)


####################################
#        Association Tables        #
####################################

students_classes = db.Table('StudentsClasses', db.Column('student_id', db.Integer, db.ForeignKey('student.id', ondelete="CASCADE", onupdate="CASCADE")), db.Column('class_id', db.Integer, db.ForeignKey('class.id', ondelete="CASCADE", onupdate="CASCADE")))

teachers_classes = db.Table('TeachersClasses', db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id', ondelete="CASCADE", onupdate="CASCADE")), db.Column('class_id', db.Integer, db.ForeignKey('class.id', ondelete="CASCADE", onupdate="CASCADE")))


####################################
#               Tables             #
####################################


class Student(BaseMixin, NameMixin, ContactMixin, db.Model):
    student_id = db.Column(db.CHAR(StudentIDLength), unique=True)
    home_language = db.Column("Language Spoken at Home", db.VARCHAR(StandardLength))
    grade_band = db.Column('Grade', db.SmallInteger, index=True)
    date_entered = db.Column("Date Entered", db.DATE, index=True)
    start_grade = db.Column("Start Grade", db.SmallInteger)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref=backref("Student", uselist=False))
    family_income = db.Column("Family Income", db.Integer, index=True)
    score = db.relationship('Score', backref='Student', lazy='dynamic')
    classes = db.relationship('Class', secondary=students_classes, cascade="all,delete")

    def __repr__(self):
        return "<{}, {} {}>".format(self.studentID, self.first, self.last)


class Teacher(BaseMixin, NameMixin, ContactMixin, db.Model):
    teacher_id = db.Column(db.CHAR(StandardLength), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    user = db.relationship("User", backref=backref("Teacher", uselist=False))
    classes = db.relationship('Class', secondary=teachers_classes, cascade="all,delete")


class Class(BaseMixin, db.Model):
    class_id = db.Column(db.CHAR(StandardLength), unique=True)
    name = db.Column(db.VARCHAR(StandardLength), index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    assignment = db.relationship("Assignment", backref="Class")
    assignment_category = db.relationship("AssignmentCategory", backref="Class")
    students = db.relationship("Student", secondary=students_classes, backref='Class')
    teachers = db.relationship("Teacher", secondary=teachers_classes, backref='Class')
    in_session = db.Column(db.Boolean, nullable=False, default=True)
