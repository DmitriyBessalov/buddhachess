"""4

Revision ID: 9b27b3b39448
Revises: c9f615c2bc49
Create Date: 2021-11-15 21:16:55.430642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b27b3b39448'
down_revision = 'c9f615c2bc49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_position', sa.Integer(), nullable=True),
    sa.Column('while_user_id', sa.Integer(), nullable=True),
    sa.Column('black_user_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('moves', sa.String(), nullable=True),
    sa.Column('move_time', sa.Integer(), nullable=True),
    sa.Column('move_time_end', sa.Integer(), nullable=True),
    sa.Column('while_time_end', sa.Integer(), nullable=True),
    sa.Column('black_time_end', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_start_position',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('chess_variant', sa.String(), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('position_FEN', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game_status',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game_status')
    op.drop_table('game_start_position')
    op.drop_table('game')
    # ### end Alembic commands ###
