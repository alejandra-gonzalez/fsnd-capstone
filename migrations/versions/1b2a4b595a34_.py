"""empty message

Revision ID: 1b2a4b595a34
Revises: 772ed70570c8
Create Date: 2021-08-09 16:04:40.693034

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1b2a4b595a34'
down_revision = '772ed70570c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('apparelItem', 'target_demographic',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('apparelItem', 'color',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('apparelItem', 'item_name',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('apparelItem', 'price',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.alter_column('order', 'customer_name',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('order', 'ship_city',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('order', 'ship_state',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('order', 'billing_city',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('order', 'billing_state',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('order', 'order_date',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order', 'order_date',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    op.alter_column('order', 'billing_state',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('order', 'billing_city',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('order', 'ship_state',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('order', 'ship_city',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('order', 'customer_name',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('apparelItem', 'price',
                    existing_type=sa.INTEGER(),
                    nullable=True)
    op.alter_column('apparelItem', 'item_name',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('apparelItem', 'color',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.alter_column('apparelItem', 'target_demographic',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    # ### end Alembic commands ###
