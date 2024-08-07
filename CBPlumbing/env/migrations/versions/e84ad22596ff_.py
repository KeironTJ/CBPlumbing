"""empty message

Revision ID: e84ad22596ff
Revises: bb5d129a680f
Create Date: 2024-03-04 21:44:56.616440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e84ad22596ff'
down_revision = 'bb5d129a680f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('item_quantity', sa.Float(precision=120), nullable=False))
        batch_op.create_index(batch_op.f('ix_job_item_item_quantity'), ['item_quantity'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_item', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_item_item_quantity'))
        batch_op.drop_column('item_quantity')

    # ### end Alembic commands ###
