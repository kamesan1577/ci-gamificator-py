"""initial migration

Revision ID: 4f6d5474da8b
Revises: 
Create Date: 2024-07-09 21:24:39.441329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f6d5474da8b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('developers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('total_points', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_developers_id'), 'developers', ['id'], unique=False)
    op.create_index(op.f('ix_developers_name'), 'developers', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_table('repositories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['developers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_index(op.f('ix_repositories_id'), 'repositories', ['id'], unique=False)
    op.create_index(op.f('ix_repositories_name'), 'repositories', ['name'], unique=False)
    op.create_table('test_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('developer_name', sa.String(), nullable=True),
    sa.Column('code_diff', sa.String(), nullable=True),
    sa.Column('coverage', sa.Float(), nullable=True),
    sa.Column('coverage_change', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('developer_id', sa.Integer(), nullable=True),
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['developer_id'], ['developers.id'], ),
    sa.ForeignKeyConstraint(['repository_id'], ['repositories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_results_developer_name'), 'test_results', ['developer_name'], unique=False)
    op.create_index(op.f('ix_test_results_id'), 'test_results', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_test_results_id'), table_name='test_results')
    op.drop_index(op.f('ix_test_results_developer_name'), table_name='test_results')
    op.drop_table('test_results')
    op.drop_index(op.f('ix_repositories_name'), table_name='repositories')
    op.drop_index(op.f('ix_repositories_id'), table_name='repositories')
    op.drop_table('repositories')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_developers_name'), table_name='developers')
    op.drop_index(op.f('ix_developers_id'), table_name='developers')
    op.drop_table('developers')
    # ### end Alembic commands ###