"""add_owner_id_column

Revision ID: 35d4dbd00f8b
Revises: 7a227a9b76b5
Create Date: 2024-11-06 09:09:35.630827

"""
from alembic import op
import sqlalchemy as sa

from project.core.config import settings


# revision identifiers, used by Alembic.
revision = '35d4dbd00f8b'
down_revision = '7a227a9b76b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('apartments', sa.Column('owner_id', sa.Integer(), server_default='-1', nullable=False), schema=settings.POSTGRES_SCHEMA)


def downgrade():
    op.drop_column('apartments', 'owner_id', schema=settings.POSTGRES_SCHEMA)