"""Add advance_amount to saved_measurement table

Revision ID: add_advance_amount_to_measurements
Revises: 
Create Date: 2025-09-09 11:40:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_advance_amount_to_measurements'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add advance_amount column to saved_measurement table
    op.add_column('saved_measurement', 
                 sa.Column('advance_amount', sa.Float(), nullable=True, server_default='0.0'))

def downgrade():
    # Remove advance_amount column
    op.drop_column('saved_measurement', 'advance_amount')
