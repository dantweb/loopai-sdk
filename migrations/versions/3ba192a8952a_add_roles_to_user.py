"""Add roles to user

Revision ID: 3ba192a8952a
Revises: f154bf7cf28e
Create Date: 2024-06-24 11:44:41.346419

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '3ba192a8952a'
down_revision = 'f154bf7cf28e'
branch_labels = None
depends_on = None

# Create an Enum type
user_role_enum = postgresql.ENUM('ADMIN', 'USER', 'GUEST', name='userrole')

def upgrade():
    # Create the Enum type in the database
    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Add the role column with the Enum type
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', user_role_enum, nullable=True))

    with op.batch_alter_table('loop', schema=None) as batch_op:
        batch_op.alter_column('project_id',
                              existing_type=sa.INTEGER(),
                              nullable=False)


def downgrade():
    # Drop the role column
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    with op.batch_alter_table('loop', schema=None) as batch_op:
        batch_op.alter_column('project_id',
                              existing_type=sa.INTEGER(),
                              nullable=True)

    # Drop the Enum type from the database
    user_role_enum.drop(op.get_bind(), checkfirst=True)
