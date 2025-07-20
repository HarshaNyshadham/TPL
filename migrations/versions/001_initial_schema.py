"""Initial database schema

Revision ID: 001_initial_schema
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create user table if it doesn't exist
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(length=120), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint('id')
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

    # Create appointable table
    op.create_table('appointable',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team', sa.String(length=100), nullable=False),
        sa.Column('division', sa.Float(), nullable=False),
        sa.Column('group', sa.String(length=1), nullable=True),
        sa.Column('game_type', sa.String(length=20), nullable=True),
        sa.Column('season_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['season_id'], ['season.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create schedule table
    op.create_table('schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team1', sa.String(length=100), nullable=False),
        sa.Column('team2', sa.String(length=100), nullable=False),
        sa.Column('division', sa.Float(), nullable=False),
        sa.Column('game_type', sa.String(length=20), nullable=True),
        sa.Column('season_id', sa.Integer(), nullable=True),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['season_id'], ['season.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('schedule')
    op.drop_table('appointable')
    op.drop_table('player')
    op.drop_table('season')
    op.drop_table('user') 