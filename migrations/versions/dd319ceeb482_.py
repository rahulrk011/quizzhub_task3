"""empty message

Revision ID: dd319ceeb482
Revises: c90997eb0b59
Create Date: 2023-07-17 18:39:54.303140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd319ceeb482'
down_revision = 'c90997eb0b59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_ques', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['op1'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_ques', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
