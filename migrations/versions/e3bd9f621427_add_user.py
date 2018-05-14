"""add_user

Revision ID: e3bd9f621427
Revises: 5a8606cd334b
Create Date: 2018-04-19 18:49:59.136407

"""
from alembic import op
from sqlalchemy_utils import ChoiceType

import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3bd9f621427'
down_revision = '5a8606cd334b'
branch_labels = None
depends_on = None

ROLES = [
    (u'superuser', u'Superuser'),
    (u'user', u'User')
]

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', ChoiceType(ROLES), nullable=True),
    sa.Column('users', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['users'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_column(u'person', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'person', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_table('role')
    op.drop_table('user')
    # ### end Alembic commands ###
