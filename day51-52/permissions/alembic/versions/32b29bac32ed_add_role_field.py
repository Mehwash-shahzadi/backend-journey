"""Add role field

Revision ID: 32b29bac32ed
Revises: b6318ce6927d
Create Date: 2025-12-13 00:26:56.712157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32b29bac32ed'
down_revision: Union[str, None] = 'b6318ce6927d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add column as nullable first
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))

    # Step 2: Update existing rows with default value
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")

    # Step 3: Alter column to NOT NULL
    op.alter_column('users', 'role', nullable=False)


def downgrade():
    op.drop_column('users', 'role')
