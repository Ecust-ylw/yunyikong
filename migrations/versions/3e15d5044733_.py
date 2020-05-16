"""empty message

Revision ID: 3e15d5044733
Revises: bcf47d4a4b8e
Create Date: 2020-05-13 12:45:11.189836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e15d5044733'
down_revision = 'bcf47d4a4b8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipment_g',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment_g')
    # ### end Alembic commands ###