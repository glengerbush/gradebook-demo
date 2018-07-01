"""init migration

Revision ID: a01e53bcd54e
Revises: 
Create Date: 2018-06-25 19:37:17.593827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a01e53bcd54e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('email_confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('registered', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_user_registered'), 'user', ['registered'], unique=False)
    op.create_table('class',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.CHAR(length=128), nullable=True),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('subject_id', sa.Integer(), nullable=True),
    sa.Column('in_session', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['subject_id'], ['subject.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('class_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Street Address', sa.VARCHAR(length=128), nullable=True),
    sa.Column('apt', sa.VARCHAR(length=32), nullable=True),
    sa.Column('city', sa.VARCHAR(length=128), nullable=True),
    sa.Column('state', sa.CHAR(length=2), nullable=True),
    sa.Column('Zip Code', sa.Integer(), nullable=True),
    sa.Column('neighborhood', sa.VARCHAR(length=128), nullable=True),
    sa.Column('Phone', sa.VARCHAR(length=12), nullable=True),
    sa.Column('Secondary Phone', sa.VARCHAR(length=12), nullable=True),
    sa.Column('email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('Secondary Email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('first', sa.VARCHAR(length=128), nullable=True),
    sa.Column('last', sa.VARCHAR(length=128), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('student_id', sa.CHAR(length=8), nullable=True),
    sa.Column('Language Spoken at Home', sa.VARCHAR(length=128), nullable=True),
    sa.Column('Grade', sa.SmallInteger(), nullable=True),
    sa.Column('Date Entered', sa.DATE(), nullable=True),
    sa.Column('Start Grade', sa.SmallInteger(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('Family Income', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_index(op.f('ix_student_Date Entered'), 'student', ['Date Entered'], unique=False)
    op.create_index(op.f('ix_student_Family Income'), 'student', ['Family Income'], unique=False)
    op.create_index(op.f('ix_student_Grade'), 'student', ['Grade'], unique=False)
    op.create_index(op.f('ix_student_Phone'), 'student', ['Phone'], unique=False)
    op.create_index(op.f('ix_student_Secondary Email'), 'student', ['Secondary Email'], unique=False)
    op.create_index(op.f('ix_student_Secondary Phone'), 'student', ['Secondary Phone'], unique=False)
    op.create_index(op.f('ix_student_Street Address'), 'student', ['Street Address'], unique=False)
    op.create_index(op.f('ix_student_Zip Code'), 'student', ['Zip Code'], unique=False)
    op.create_index(op.f('ix_student_apt'), 'student', ['apt'], unique=False)
    op.create_index(op.f('ix_student_city'), 'student', ['city'], unique=False)
    op.create_index(op.f('ix_student_dob'), 'student', ['dob'], unique=False)
    op.create_index(op.f('ix_student_email'), 'student', ['email'], unique=False)
    op.create_index(op.f('ix_student_first'), 'student', ['first'], unique=False)
    op.create_index(op.f('ix_student_last'), 'student', ['last'], unique=False)
    op.create_index(op.f('ix_student_neighborhood'), 'student', ['neighborhood'], unique=False)
    op.create_index(op.f('ix_student_state'), 'student', ['state'], unique=False)
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Street Address', sa.VARCHAR(length=128), nullable=True),
    sa.Column('apt', sa.VARCHAR(length=32), nullable=True),
    sa.Column('city', sa.VARCHAR(length=128), nullable=True),
    sa.Column('state', sa.CHAR(length=2), nullable=True),
    sa.Column('Zip Code', sa.Integer(), nullable=True),
    sa.Column('neighborhood', sa.VARCHAR(length=128), nullable=True),
    sa.Column('Phone', sa.VARCHAR(length=12), nullable=True),
    sa.Column('Secondary Phone', sa.VARCHAR(length=12), nullable=True),
    sa.Column('email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('Secondary Email', sa.VARCHAR(length=128), nullable=True),
    sa.Column('first', sa.VARCHAR(length=128), nullable=True),
    sa.Column('last', sa.VARCHAR(length=128), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('teacher_id', sa.CHAR(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('teacher_id')
    )
    op.create_index(op.f('ix_teacher_Phone'), 'teacher', ['Phone'], unique=False)
    op.create_index(op.f('ix_teacher_Secondary Email'), 'teacher', ['Secondary Email'], unique=False)
    op.create_index(op.f('ix_teacher_Secondary Phone'), 'teacher', ['Secondary Phone'], unique=False)
    op.create_index(op.f('ix_teacher_Street Address'), 'teacher', ['Street Address'], unique=False)
    op.create_index(op.f('ix_teacher_Zip Code'), 'teacher', ['Zip Code'], unique=False)
    op.create_index(op.f('ix_teacher_apt'), 'teacher', ['apt'], unique=False)
    op.create_index(op.f('ix_teacher_city'), 'teacher', ['city'], unique=False)
    op.create_index(op.f('ix_teacher_dob'), 'teacher', ['dob'], unique=False)
    op.create_index(op.f('ix_teacher_email'), 'teacher', ['email'], unique=False)
    op.create_index(op.f('ix_teacher_first'), 'teacher', ['first'], unique=False)
    op.create_index(op.f('ix_teacher_last'), 'teacher', ['last'], unique=False)
    op.create_index(op.f('ix_teacher_neighborhood'), 'teacher', ['neighborhood'], unique=False)
    op.create_index(op.f('ix_teacher_state'), 'teacher', ['state'], unique=False)
    op.create_index(op.f('ix_teacher_user_id'), 'teacher', ['user_id'], unique=False)
    op.create_table('user_roles',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    op.create_table('StudentsClasses',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], onupdate='CASCADE', ondelete='CASCADE')
    )
    op.create_table('TeachersClasses',
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], onupdate='CASCADE', ondelete='CASCADE')
    )
    op.create_table('assignmentcategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.VARCHAR(length=64), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignmentcategory_category'), 'assignmentcategory', ['category'], unique=False)
    op.create_index(op.f('ix_assignmentcategory_weight'), 'assignmentcategory', ['weight'], unique=False)
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('Start', sa.TIMESTAMP(), nullable=True),
    sa.Column('Arrived', sa.TIMESTAMP(), nullable=True),
    sa.Column('session', sa.SmallInteger(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendance_Arrived'), 'attendance', ['Arrived'], unique=False)
    op.create_index(op.f('ix_attendance_Start'), 'attendance', ['Start'], unique=False)
    op.create_index(op.f('ix_attendance_class_id'), 'attendance', ['class_id'], unique=False)
    op.create_index(op.f('ix_attendance_session'), 'attendance', ['session'], unique=False)
    op.create_index(op.f('ix_attendance_student_id'), 'attendance', ['student_id'], unique=False)
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=128), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('assignment_category_id', sa.Integer(), nullable=True),
    sa.Column('total_points', sa.Integer(), nullable=True),
    sa.Column('Date', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['assignment_category_id'], ['assignmentcategory.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assignment_Date'), 'assignment', ['Date'], unique=False)
    op.create_index(op.f('ix_assignment_name'), 'assignment', ['name'], unique=False)
    op.create_table('score',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assignment_id'], ['assignment.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('student_id', 'assignment_id'),
    sa.UniqueConstraint('student_id', 'assignment_id', name='score_id')
    )
    op.create_index(op.f('ix_score_score'), 'score', ['score'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_score_score'), table_name='score')
    op.drop_table('score')
    op.drop_index(op.f('ix_assignment_name'), table_name='assignment')
    op.drop_index(op.f('ix_assignment_Date'), table_name='assignment')
    op.drop_table('assignment')
    op.drop_index(op.f('ix_attendance_student_id'), table_name='attendance')
    op.drop_index(op.f('ix_attendance_session'), table_name='attendance')
    op.drop_index(op.f('ix_attendance_class_id'), table_name='attendance')
    op.drop_index(op.f('ix_attendance_Start'), table_name='attendance')
    op.drop_index(op.f('ix_attendance_Arrived'), table_name='attendance')
    op.drop_table('attendance')
    op.drop_index(op.f('ix_assignmentcategory_weight'), table_name='assignmentcategory')
    op.drop_index(op.f('ix_assignmentcategory_category'), table_name='assignmentcategory')
    op.drop_table('assignmentcategory')
    op.drop_table('TeachersClasses')
    op.drop_table('StudentsClasses')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_teacher_user_id'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_state'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_neighborhood'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_last'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_first'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_email'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_dob'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_city'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_apt'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_Zip Code'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_Street Address'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_Secondary Phone'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_Secondary Email'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_Phone'), table_name='teacher')
    op.drop_table('teacher')
    op.drop_index(op.f('ix_student_state'), table_name='student')
    op.drop_index(op.f('ix_student_neighborhood'), table_name='student')
    op.drop_index(op.f('ix_student_last'), table_name='student')
    op.drop_index(op.f('ix_student_first'), table_name='student')
    op.drop_index(op.f('ix_student_email'), table_name='student')
    op.drop_index(op.f('ix_student_dob'), table_name='student')
    op.drop_index(op.f('ix_student_city'), table_name='student')
    op.drop_index(op.f('ix_student_apt'), table_name='student')
    op.drop_index(op.f('ix_student_Zip Code'), table_name='student')
    op.drop_index(op.f('ix_student_Street Address'), table_name='student')
    op.drop_index(op.f('ix_student_Secondary Phone'), table_name='student')
    op.drop_index(op.f('ix_student_Secondary Email'), table_name='student')
    op.drop_index(op.f('ix_student_Phone'), table_name='student')
    op.drop_index(op.f('ix_student_Grade'), table_name='student')
    op.drop_index(op.f('ix_student_Family Income'), table_name='student')
    op.drop_index(op.f('ix_student_Date Entered'), table_name='student')
    op.drop_table('student')
    op.drop_table('class')
    op.drop_index(op.f('ix_user_registered'), table_name='user')
    op.drop_table('user')
    op.drop_table('subject')
    op.drop_table('roles')
    # ### end Alembic commands ###