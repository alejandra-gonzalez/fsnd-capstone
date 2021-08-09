"""empty message

Revision ID: 772ed70570c8
Revises: 
Create Date: 2021-08-09 15:45:33.787888

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '772ed70570c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('OrderItems')
    op.drop_table('Orders')
    op.drop_table('ApparelItems')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apparelItem',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"ApparelItems_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('target_demographic', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('color', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('item_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('released', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='ApparelItems_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('orderItem',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"OrderItems_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['ApparelItems.id'], name='OrderItems_item_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], ['Orders.id'], name='OrderItems_order_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='OrderItems_pkey')
    )
    op.create_table('order',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Orders_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('customer_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('ship_city', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('ship_state', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('billing_city', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('billing_state', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('order_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Orders_pkey')
    )
    # ### end Alembic commands ###
