"""initial_revision

Revision ID: d01d118f7d4a
Revises: 
Create Date: 2017-09-29 12:07:32.095666

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy_utils import ChoiceType


# revision identifiers, used by Alembic.
revision = 'd01d118f7d4a'
down_revision = None
branch_labels = None
depends_on = None

DEVICES = [
        (u'mobile', u'Mobile'),
        (u'laptop', u'Laptop'),
        (u'desktop', u'Desktop')
    ]

def upgrade():
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('last_name', sa.String(length=128), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('address',
    sa.Column('mac', sa.String(length=128), nullable=False),
    sa.Column('device', ChoiceType(DEVICES), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.PrimaryKeyConstraint('mac')
    )
    op.create_table('entry',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mac_id', sa.String(length=128), nullable=True),
    sa.Column('startdate', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['mac_id'], ['address.mac'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('entry')
    op.drop_table('address')
    op.drop_table('person')
