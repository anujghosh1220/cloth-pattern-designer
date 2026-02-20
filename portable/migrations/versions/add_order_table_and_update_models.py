"""Add Order table and update models

Revision ID: add_order_table
Revises: 
Create Date: 2025-09-09 12:59:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_order_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Rename amount to total_amount in customer table
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('amount', new_column_name='total_amount', existing_type=sa.Float(), 
                           existing_nullable=True, existing_server_default=sa.text('0.0'))
    
    # Create order table
    op.create_table('order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('advance_amount', sa.Float(), server_default='0.0'),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('order_date', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE')),
        sa.Column('delivery_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), 
                 onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add order_id to saved_measurement table
    with op.batch_alter_table('saved_measurement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('order_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_saved_measurement_order_id', 'saved_measurement', 'order', ['order_id'], ['id'])

def downgrade():
    # Remove order_id from saved_measurement
    with op.batch_alter_table('saved_measurement', schema=None) as batch_op:
        batch_op.drop_constraint('fk_saved_measurement_order_id', type_='foreignkey')
        batch_op.drop_column('order_id')
    
    # Drop order table
    op.drop_table('order')
    
    # Revert customer table changes
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('total_amount', new_column_name='amount', existing_type=sa.Float(), 
                           existing_nullable=True, existing_server_default=sa.text('0.0'))
