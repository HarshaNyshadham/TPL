"""Add Player model and game type support

Revision ID: add_player_and_game_type
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_player_and_game_type'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create player table
    op.create_table('player',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('partner_name', sa.String(length=100), nullable=True),
        sa.Column('game_type', sa.String(length=20), nullable=False),
        sa.Column('division', sa.Float(), nullable=True),
        sa.Column('group', sa.String(length=1), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Add game_type to appointable table
    op.add_column('appointable',
        sa.Column('game_type', sa.String(length=20), nullable=True)
    )
    op.add_column('appointable',
        sa.Column('season_id', sa.Integer(), nullable=True)
    )

    # Add game_type to schedule table
    op.add_column('schedule',
        sa.Column('game_type', sa.String(length=20), nullable=True)
    )
    op.add_column('schedule',
        sa.Column('season_id', sa.Integer(), nullable=True)
    )

    # Create season table
    op.create_table('season',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )

    # Add foreign key constraints
    op.create_foreign_key(None, 'appointable', 'season', ['season_id'], ['id'])
    op.create_foreign_key(None, 'schedule', 'season', ['season_id'], ['id'])

def downgrade():
    # Remove foreign key constraints
    op.drop_constraint(None, 'schedule', type_='foreignkey')
    op.drop_constraint(None, 'appointable', type_='foreignkey')

    # Drop season table
    op.drop_table('season')

    # Remove game_type and season_id from schedule table
    op.drop_column('schedule', 'season_id')
    op.drop_column('schedule', 'game_type')

    # Remove game_type and season_id from appointable table
    op.drop_column('appointable', 'season_id')
    op.drop_column('appointable', 'game_type')

    # Drop player table
    op.drop_table('player') 