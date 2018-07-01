"""test

Revision ID: 221a03a18e77
Revises: 97aa2ab507fc
Create Date: 2018-06-30 14:10:06.669294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '221a03a18e77'
down_revision = '97aa2ab507fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('score_id', 'score', type_='unique')
    op.create_unique_constraint('score_id', 'score', ['student_id', 'assignment_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('score_id', 'score', type_='unique')
    # ### end Alembic commands ###