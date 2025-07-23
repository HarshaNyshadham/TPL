"""
Alembic merge migration to resolve multiple heads after removing season_id from Player.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'merge_heads_remove_season_id'
down_revision = ('001_initial_schema', 'remove_season_id_from_player')
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
