"""empty message

Revision ID: b61e7cbb20b0
Revises: d260b19c5598
Create Date: 2026-03-02 16:28:24.002451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b61e7cbb20b0'
down_revision: Union[str, Sequence[str], None] = 'd260b19c5598'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
