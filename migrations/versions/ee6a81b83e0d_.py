"""empty message

Revision ID: ee6a81b83e0d
Revises: 681412ff640a
Create Date: 2020-04-23 20:29:12.314026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee6a81b83e0d'
down_revision = '681412ff640a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status', sa.Enum('正常', '异常', '疑似'), server_default='正常', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'status')
    # ### end Alembic commands ###
