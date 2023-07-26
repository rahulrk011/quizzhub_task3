"""empty message

Revision ID: 655a12047a81
Revises: fcadc395c823
Create Date: 2023-07-17 12:13:17.895666

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '655a12047a81'
down_revision = 'fcadc395c823'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_ques', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quiz_id', sa.Integer(), nullable=True))
        batch_op.alter_column('correct_option',
               existing_type=sa.VARCHAR(length=5),
               type_=sa.Integer(),
               existing_nullable=True)
        batch_op.create_unique_constraint('op', ['op1'])
        batch_op.drop_constraint('op', type_='foreignkey')
        batch_op.create_foreign_key('fkop', 'quiz', ['quiz_id'], ['id'])
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quiz_ques', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('correct_option',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=5),
               existing_nullable=True)
        batch_op.drop_column('quiz_id')

    # ### end Alembic commands ###