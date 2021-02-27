"""empty message

Revision ID: b91bbd1cd81d
Revises: 62ff5f7ce504
Create Date: 2021-02-25 18:09:41.588295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b91bbd1cd81d'
down_revision = '62ff5f7ce504'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_traveler', sa.Integer(), nullable=True),
    sa.Column('id_pro', sa.Integer(), nullable=True),
    sa.Column('id_offer', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('attached', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['id_offer'], ['offers.id'], ),
    sa.ForeignKeyConstraint(['id_pro'], ['userpro.id'], ),
    sa.ForeignKeyConstraint(['id_traveler'], ['traveler.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    # ### end Alembic commands ###