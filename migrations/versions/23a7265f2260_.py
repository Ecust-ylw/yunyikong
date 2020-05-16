"""empty message

Revision ID: 23a7265f2260
Revises: aeca8c9a26ac
Create Date: 2020-04-18 11:56:42.258926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23a7265f2260'
down_revision = 'aeca8c9a26ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('equipment', sa.Column('gaode_latitude', sa.DECIMAL(precision='15,8'), nullable=True))
    op.add_column('equipment', sa.Column('gaode_longitude', sa.DECIMAL(precision='15,8'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('equipment', 'gaode_longitude')
    op.drop_column('equipment', 'gaode_latitude')
    # ### end Alembic commands ###
