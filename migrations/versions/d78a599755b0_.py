"""empty message

Revision ID: d78a599755b0
Revises: b61e7cbb20b0
Create Date: 2026-03-02 16:40:09.018579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd78a599755b0'
down_revision: Union[str, Sequence[str], None] = 'b61e7cbb20b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
