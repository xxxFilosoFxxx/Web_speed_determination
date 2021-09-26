"""empty message

Revision ID: ab01a3a4c6c2
Revises: 1996af0d47e3
Create Date: 2021-09-22 14:47:31.698709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab01a3a4c6c2'
down_revision = '1996af0d47e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('uuid', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'uuid')
    # ### end Alembic commands ###
