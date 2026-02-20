"""add customer_id to saved_measurement

Revision ID: 1234abcd5678
Revises: 
Create Date: 2025-09-04 12:56:33.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1234abcd5678'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add customer_id column with a foreign key to customer.id
    op.add_column('saved_measurement', 
                 sa.Column('customer_id', sa.Integer(), 
                          sa.ForeignKey('customer.id', ondelete='CASCADE'), 
                          nullable=True))
    # Create an index for better query performance
    op.create_index(op.f('ix_saved_measurement_customer_id'), 
                   'saved_measurement', ['customer_id'], unique=False)

def downgrade():
    # Drop the index and column when rolling back
    op.drop_index(op.f('ix_saved_measurement_customer_id'), 
                 table_name='saved_measurement')
    op.drop_column('saved_measurement', 'customer_id')
