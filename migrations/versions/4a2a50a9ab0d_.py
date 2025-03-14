"""empty message

Revision ID: 4a2a50a9ab0d
Revises: 0091d30c1a07
Create Date: 2025-03-09 15:02:04.790122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a2a50a9ab0d'
down_revision: Union[str, None] = '0091d30c1a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('category_name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category_name')
    )
    op.create_table('courier_rating',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['user_profile.id'], ),
    sa.ForeignKeyConstraint(['courier_id'], ['user_profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('order_status', sa.Enum('awaiting_processing', 'delivered', 'process_of_delivery', 'cancelled', name='orderstatuschoicess'), nullable=False),
    sa.Column('delivery_address', sa.String(length=128), nullable=False),
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['user_profile.id'], ),
    sa.ForeignKeyConstraint(['courier_id'], ['user_profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('store_name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('store_image', sa.String(), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user_profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('combo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('combo_name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('combo_image', sa.String(), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('contact',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('contact_number', sa.String(), nullable=True),
    sa.Column('social_network', sa.String(), nullable=True),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courier',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('courier_status', sa.Enum('available', 'busy', name='courierstatuschoicess'), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['user_profile.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_name', sa.String(length=32), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('product_image', sa.String(), nullable=False),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_review',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['user_profile.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('store_review')
    op.drop_table('product')
    op.drop_table('courier')
    op.drop_table('contact')
    op.drop_table('combo')
    op.drop_table('store')
    op.drop_table('order')
    op.drop_table('courier_rating')
    op.drop_table('category')
    # ### end Alembic commands ###
