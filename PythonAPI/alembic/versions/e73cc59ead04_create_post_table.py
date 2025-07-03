"""create post table

Revision ID: e73cc59ead04
Revises: 383875e1e9b9
Create Date: 2025-07-02 19:54:42.731224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e73cc59ead04'
down_revision: Union[str, Sequence[str], None] = '383875e1e9b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
