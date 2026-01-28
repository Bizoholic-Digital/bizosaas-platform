"""
Database migration: Add workflow_proposals table and enhance workflows table
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_workflow_governance'
down_revision = None  # Update this to your latest migration
branch_labels = None
depends_on = None


def upgrade():
    # Create workflow_proposals table
    op.create_table(
        'workflow_proposals',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('proposed', 'refinement_requested', 'approved', 'rejected', 'archived', 
                                     name='workflowstatus'), nullable=False),
        sa.Column('workflow_definition', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('discovered_by', sa.String(), nullable=False),
        sa.Column('discovery_method', sa.String(), nullable=True),
        sa.Column('estimated_cost', sa.Float(), nullable=True),
        sa.Column('impact_analysis', sa.Text(), nullable=True),
        sa.Column('admin_feedback', sa.Text(), nullable=True),
        sa.Column('suggested_changes', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('approved_by', sa.String(), nullable=True),
        sa.Column('rejected_by', sa.String(), nullable=True),
        sa.Column('admin_notes', sa.Text(), nullable=True),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('rejected_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('refinement_requested_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes for common queries
    op.create_index('idx_workflow_proposals_status', 'workflow_proposals', ['status'])
    op.create_index('idx_workflow_proposals_category', 'workflow_proposals', ['category'])
    op.create_index('idx_workflow_proposals_discovered_by', 'workflow_proposals', ['discovered_by'])
    
    # Enhance workflows table
    op.add_column('workflows', sa.Column('category', sa.String(), nullable=True))
    op.add_column('workflows', sa.Column('workflow_blueprint', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.add_column('workflows', sa.Column('approved_by', sa.String(), nullable=True))
    op.add_column('workflows', sa.Column('approved_at', sa.DateTime(), nullable=True))
    
    # Set default category for existing workflows
    op.execute("UPDATE workflows SET category = 'all' WHERE category IS NULL")


def downgrade():
    # Remove columns from workflows table
    op.drop_column('workflows', 'approved_at')
    op.drop_column('workflows', 'approved_by')
    op.drop_column('workflows', 'workflow_blueprint')
    op.drop_column('workflows', 'category')
    
    # Drop indexes
    op.drop_index('idx_workflow_proposals_discovered_by', table_name='workflow_proposals')
    op.drop_index('idx_workflow_proposals_category', table_name='workflow_proposals')
    op.drop_index('idx_workflow_proposals_status', table_name='workflow_proposals')
    
    # Drop workflow_proposals table
    op.drop_table('workflow_proposals')
    
    # Drop enum type
    op.execute('DROP TYPE workflowstatus')
