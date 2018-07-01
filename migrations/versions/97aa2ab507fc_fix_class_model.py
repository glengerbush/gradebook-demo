"""fix class model

Revision ID: 97aa2ab507fc
Revises: a01e53bcd54e
Create Date: 2018-06-30 14:00:00.629046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97aa2ab507fc'
down_revision = 'a01e53bcd54e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_class_name'), 'class', ['name'], unique=False)
    op.drop_constraint(u'class_name_key', 'class', type_='unique')
    # Not sure why this line was made in this migration. commented out for now
    # op.create_unique_constraint('score_id', 'score', ['student_id', 'assignment_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('score_id', 'score', type_='unique')
    op.create_unique_constraint(u'class_name_key', 'class', ['name'])
    op.drop_index(op.f('ix_class_name'), table_name='class')
    # ### end Alembic commands ###
