"""Create chat_messages table

Revision ID: 001
Revises: 
Create Date: 2024-01-20 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create chat_messages table with indexes."""
    # Create chat_messages table
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('session_id', sa.String(length=100), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for performance
    op.create_index('idx_session_timestamp', 'chat_messages', ['session_id', 'timestamp'])
    op.create_index('idx_timestamp', 'chat_messages', ['timestamp'])
    op.create_index(op.f('ix_chat_messages_session_id'), 'chat_messages', ['session_id'])


def downgrade() -> None:
    """Drop chat_messages table and indexes."""
    op.drop_index(op.f('ix_chat_messages_session_id'), table_name='chat_messages')
    op.drop_index('idx_timestamp', table_name='chat_messages')
    op.drop_index('idx_session_timestamp', table_name='chat_messages')
    op.drop_table('chat_messages')
