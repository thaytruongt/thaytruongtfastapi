"""create table company

Revision ID: d9ac93518b59
Revises: 50a9ca6904dd
Create Date: 2024-08-28 13:45:41.408587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from schemas.company import CompanyMode


# revision identifiers, used by Alembic.
revision = 'd9ac93518b59'
down_revision = '50a9ca6904dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'companys',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('mode', sa.Enum(CompanyMode), nullable=False, default=CompanyMode.DRAFT),
        sa.Column('rating', sa.SmallInteger, default=0),
        sa.Column('owner_id', sa.UUID, nullable=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key('fk_company_user', 'companys', 'users', ['owner_id'], ['id'])

## add company_id to users table
    op.add_column("users", sa.Column("company_id", sa.UUID, nullable=True))
    op.create_foreign_key("fk_user_company", "users", "companys", ["company_id"],['id'])
    
    
def downgrade() -> None:
    
    
    # drop column company_id on users table
    op.drop_column("users", "company_id")
    #drop company table
    op.drop_table('companys')
    #drop CompanyMode
    op.execute("DROP TYPE companymode;")
