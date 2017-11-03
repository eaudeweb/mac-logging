"""add_deleted_field

Revision ID: 5a8606cd334b
Revises: d01d118f7d4a
Create Date: 2017-11-03 11:29:50.228461

"""
from alembic import op
import sqlalchemy as sa
import sqlite3


# revision identifiers, used by Alembic.
revision = '5a8606cd334b'
down_revision = 'd01d118f7d4a'
branch_labels = None
depends_on = None


def connect_to_db():
    return sqlite3.connect("/var/local/pontaj/files/mac_logging.db")


def upgrade():
    op.add_column('address', sa.Column('deleted', sa.Boolean(), nullable=True,
                                       default=False))
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("UPDATE address SET deleted=0;")
    conn.commit()
    conn.close()


def downgrade():
    conn = connect_to_db()
    c = conn.cursor()
    c.execute("CREATE TEMPORARY TABLE address_backup(mac,device,person_id);")
    c.execute("INSERT INTO address_backup SELECT mac,device,person_id FROM address;")
    c.execute("DROP TABLE address;")
    c.execute("CREATE TABLE address ("
        "mac VARCHAR(128) NOT NULL, "
        "device VARCHAR(255) NOT NULL, "
        "person_id INTEGER, "
        "PRIMARY KEY (mac), "
        "FOREIGN KEY(person_id) REFERENCES person (id));")
    c.execute("INSERT INTO address SELECT mac,device,person_id FROM address_backup;")
    c.execute("DROP TABLE address_backup;")
    conn.commit()
    conn.close()
