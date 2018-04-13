"""add_user

Revision ID: e29a6e57b697
Revises: 5a8606cd334b
Create Date: 2018-01-18 14:15:57.412503

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import ChoiceType


# revision identifiers, used by Alembic.
revision = 'e29a6e57b697'
down_revision = '5a8606cd334b'
branch_labels = None
depends_on = None

ROLES = [
        (u'superuser', u'Superuser'),
        (u'user', u'User')
    ]

def upgrade():
    # import pdb; pdb.set_trace()
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
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
    op.add_column(u'person', sa.Column('user', sa.Integer(), nullable=True))
    #TODO I have a problem at this line "No support for ALTER of constraints in SQLite dialect"
    op.create_foreign_key('fk_user_person', 'user', 'person', ['id'], ['user_id'])


def downgrade():
    op.drop_constraint(None, 'person', type_='foreignkey')
    op.drop_column(u'person', 'user_id')
    op.drop_table('role')
    op.drop_table('user')
