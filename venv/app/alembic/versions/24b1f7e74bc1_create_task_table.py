"""create table task

Revision ID: 24b1f7e74bc1
Revises: d9ac93518b59
Create Date: 2024-08-28 13:52:15.943842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24b1f7e74bc1'
down_revision= 'd9ac93518b59'
branch_labels= None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status', sa.String),
        sa.Column('priority', sa.Integer, default=3),
        sa.Column('owner_id', sa.UUID, nullable=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_task_user', 'tasks', 'users', ['owner_id'], ['id'])

def downgrade() -> None:
      op.drop_table('tasks')
    
