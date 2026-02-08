"""Change user_id from UUID to String in user_mcp_installations

Revision ID: fix_clerk_user_id
Revises: 
Create Date: 2026-01-10 04:25:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fix_clerk_user_id'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop the foreign key constraint first
    op.drop_constraint('user_mcp_installations_user_id_fkey', 'user_mcp_installations', type_='foreignkey')
    
    # Change the column type from UUID to String
    op.alter_column('user_mcp_installations', 'user_id',
                    existing_type=postgresql.UUID(),
                    type_=sa.String(length=255),
                    existing_nullable=False)
    
    # Add index for performance
    op.create_index(op.f('ix_user_mcp_installations_user_id'), 'user_mcp_installations', ['user_id'], unique=False)


def downgrade():
    # Remove the index
    op.drop_index(op.f('ix_user_mcp_installations_user_id'), table_name='user_mcp_installations')
    
    # Change back to UUID
    op.alter_column('user_mcp_installations', 'user_id',
                    existing_type=sa.String(length=255),
                    type_=postgresql.UUID(),
                    existing_nullable=False,
                    postgresql_using='user_id::uuid')
    
    # Re-add the foreign key constraint
    op.create_foreign_key('user_mcp_installations_user_id_fkey', 
                         'user_mcp_installations', 'users', 
                         ['user_id'], ['id'], 
                         ondelete='CASCADE')
