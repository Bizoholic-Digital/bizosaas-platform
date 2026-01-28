"""
Database migration: Add workflow_executions table for monitoring
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_workflow_executions'
down_revision = 'add_workflow_governance'
branch_labels = None
depends_on = None


def upgrade():
    # Create workflow_executions table
    op.create_table(
        'workflow_executions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('workflow_id', sa.String(), nullable=False),
        sa.Column('workflow_name', sa.String(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('steps_total', sa.Integer(), default=0),
        sa.Column('steps_completed', sa.Integer(), default=0),
        sa.Column('steps_failed', sa.Integer(), default=0),
        sa.Column('failed_step', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('error_stack_trace', sa.Text(), nullable=True),
        sa.Column('cost_estimate', sa.Float(), default=0.0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add indexes for common queries
    op.create_index('idx_workflow_executions_workflow_id', 'workflow_executions', ['workflow_id'])
    op.create_index('idx_workflow_executions_tenant_id', 'workflow_executions', ['tenant_id'])
    op.create_index('idx_workflow_executions_status', 'workflow_executions', ['status'])
    op.create_index('idx_workflow_executions_started_at', 'workflow_executions', ['started_at'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_workflow_executions_started_at', table_name='workflow_executions')
    op.drop_index('idx_workflow_executions_status', table_name='workflow_executions')
    op.drop_index('idx_workflow_executions_tenant_id', table_name='workflow_executions')
    op.drop_index('idx_workflow_executions_workflow_id', table_name='workflow_executions')
    
    # Drop workflow_executions table
    op.drop_table('workflow_executions')
